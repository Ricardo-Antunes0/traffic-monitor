from django.db import models

#
# Vamos ter 2 modelos:
# - RoadSegment
# - SpeedReading

# RoadSegment 


class RoadSegment(models.Model):
    """
    Segmento de estrada contendo as respetivas coordenadas geográficas (lat,lng).
    """

    longitude_start = models.FloatField(verbose_name="Longitude de Início")     # Longitude inicial
    latitude_start = models.FloatField(verbose_name="Latitude de Início")       # Latitude inicial
    longitude_end = models.FloatField(verbose_name="Longitude de Fim")          # Longitude final
    latitude_end = models.FloatField(verbose_name="Latitude de Fim")            # Latitude final
    length = models.FloatField(verbose_name="Comprimento (metros)")             # Comprimento do segmento
    created_at = models.DateTimeField(auto_now_add=True)                        # Guarda automaticamente quando o segemento de estrada for criado
    updated_at = models.DateTimeField(auto_now=True)                            # Atualiza automaticamente quando o segmento de estrada for modificado
    
    class Meta:
        db_table = 'road_segments'                      # Nome da tabela
        ordering = ['id']                               # Ordenar pelo ID
        verbose_name = 'Segmento de Estrada'
        verbose_name_plural = 'Segmentos de Estrada'
    
    def __str__(self):
        return f"Segmento {self.id}"    # Exemplo: Segmento 1


class SpeedReading(models.Model):
    """
    Leitura de velocidade média de um dado segmento de estrada.
    A intensidade do trânsito será calculada posteriormente.
    """

    road_segment = models.ForeignKey(
        RoadSegment,
        on_delete=models.CASCADE,       # Se o segmento for apagado, todas os objetos associados a ele também serão
        related_name='readings',
        verbose_name='Segmento de Estrada'
    )
    average_speed = models.FloatField(verbose_name="Velocidade Média (km/h)")   # Velocidade média dos veículos no segmento associado
    timestamp = models.DateTimeField(verbose_name="Data/Hora da Leitura")       # Para saber o omento real em que a leitura foi feita no trânsito
    created_at = models.DateTimeField(auto_now_add=True)                        # Data de criação desta leitura de velocidade na db
    
    class Meta:
        db_table = 'speed_readings'             # Nome da tabela        
        ordering = ['-timestamp']               # Ordenar começando do mais recente para o mais antigo
        verbose_name = 'Leitura de Velocidade'
        verbose_name_plural = 'Leituras de Velocidade'
    
    def __str__(self):
        return f"Leitura {self.id} - {self.average_speed} km/h"     # Por Exemplo: Leitura 3 - 40.5 km/h
    
    @property
    def intensity(self):
        """
        Serve para calcular a intensidade do tráfego.
        Este atributo não será guardado na base de dados
        """
        if self.average_speed <= 20:
            return "elevada"
        elif self.average_speed <= 50:
            return "média"
        else:
            return "baixa"


