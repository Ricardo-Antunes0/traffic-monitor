import csv
from django.core.management.base import BaseCommand
from django.utils import timezone
from traffic_monitor.models import RoadSegment, SpeedReading


class Command(BaseCommand):
    """
    Comando Django para importar dados de um ficheiro CSV para a db.
    
    Como Utilizar:
        python manage.py import_data
    
    Passos:
        1. Lê o ficheiro data/traffic_speed.csv
        2. Para cada linha:
           - Cria ou obtêm um RoadSegment (segmento de estrada)
           - Cria uma SpeedReading associado a esse segmento
        3. Mostra logs no final

    Nota: 
        - IDs são gerados automaticamente pelo PostgreSQL
        - Evitamos problemas de sequência desatualizada ao fazer o import
    """

    help = 'Importa dados do ficheiro traffic_speed.csv para a base de dados'
    
    def handle(self, *args, **options):
        """
        Método principal executado pelo Django quando o comando é chamado.
        """
        
        csv_file = 'data/traffic_speed.csv' # Caminho para o ficheiro CSV
    
        # Contadores para estatística
        segments_created = 0  # Número de segmentos criados
        readings_created = 0  # Número de leituras criadas
        errors = 0            # Número de erros ocorridos

        self.stdout.write(self.style.WARNING(f'A iniciar importação de {csv_file}..\n'))
        
        try:
            # Abre o ficheiro CSV em modo leitura com codificação UTF-8
            with open(csv_file, 'r', encoding='utf-8') as file:  
                # DictReader transforma cada linha do CSV num dicionário
                # Exemplo de um dado: {'ID': '1', 'Long_start': '103.946', 'Lat_start': '30.750', ...}
                reader = csv.DictReader(file, delimiter=',')
            
                for row in reader:
                    try:
                        # ===== EXTRAIR DADOS DA LINHA =====
                        segment_id = int(row['ID'])
                        longitude_start = float(row['Long_start'])
                        latitude_start = float(row['Lat_start'])
                        longitude_end = float(row['Long_end'])
                        latitude_end = float(row['Lat_end'])
                        length = float(row['Length'])
                        speed = float(row['Speed'])
                        
                        # ===== CRIAR OU OBTER SEGMENTO DE ESTRADA =====
                        # Procurar segmento existente com as mesmas coordenadas
                        existing = RoadSegment.objects.filter(
                            longitude_start=longitude_start,
                            latitude_start=latitude_start,
                            longitude_end=longitude_end,
                            latitude_end=latitude_end
                        ).first()

                        if existing:
                            segment = existing  # Segmento já existe, usa o existente
                        else:
                            segment = RoadSegment.objects.create(
                                longitude_start=longitude_start,
                                latitude_start=latitude_start,
                                longitude_end=longitude_end,
                                latitude_end=latitude_end,
                                length=length,
                            )
                            segments_created += 1
                        
                        # ===== CRIAR LEITURA DE VELOCIDADE =====
                        reading = SpeedReading.objects.create(
                            road_segment=segment,      # FK para o segmento
                            average_speed=speed,       # Velocidade do CSV
                            timestamp=timezone.now()   # Data/hora atual
                        )
                        
                        readings_created += 1
                        
                        # ===== MOSTRAR PROGRESSO =====
                        
                        #  Mostrar progresso a cada 50 segmentos criados
                        if segments_created % 50 == 0 and segments_created > 0:
                            self.stdout.write(f' Já foram processados {segments_created} segmentos!')
                    
                    # Se a coluna não existe no CSV
                    except KeyError as e:
                        errors += 1
                        self.stdout.write(self.style.ERROR(f'Erro: Coluna {e} não encontrada na linha'))
                        continue
                    # Se não conseguiu converter a string para número (int ou float)
                    except ValueError as e:
                        errors += 1
                        self.stdout.write(self.style.ERROR(f'Erro ao converter dados: {e}'))
                        continue
                    # Em caso qualquer outro erro
                    except Exception as e:
                        errors += 1
                        self.stdout.write(self.style.ERROR(f'Erro inesperado na linha {row.get("ID", "?")}: {e}'))
                        continue
            
            # ===== DADOS FINAIS =====
            self.stdout.write('\n' + '='*60)
            self.stdout.write(self.style.SUCCESS('Importação concluída!'))
            self.stdout.write('='*60)
            self.stdout.write(self.style.SUCCESS(f'Segmentos criados: {segments_created}'))
            self.stdout.write(self.style.SUCCESS(f'Leituras criadas: {readings_created}'))
            
            if errors > 0:
                self.stdout.write(self.style.ERROR(f'Ocorreram {errors} erros'))
            else:
                self.stdout.write(self.style.SUCCESS('Não houve erros!!!'))
            self.stdout.write('='*60 + '\n')
        # Se o ficheiro não existir
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'\n Erro: Ficheiro não encontrado: {csv_file}'))
            self.stdout.write(self.style.WARNING('Certifica-te que o ficheiro está na pasta data/ \n '))
        # Qualquer outro erro
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n Erro durante importação: {e}\n'))