from rest_framework import serializers
from .models import RoadSegment, speed_readings


class SpeedReadingSerializer(serializers.ModelSerializer):

    """
    Serializer para o modelo SpeedReading (leituras de velocidade).
    
    Converte o objeto Python em JSON e vice-versa.
    Para alem disso, também é adicionado o campo intensidade.
    """

    # Este campo é apenas de leitura, uma vez que é calculado pela propriedade criada neste modelo
    intensity = serializers.ReadOnlyField()

    class Meta: 
        model = SpeedReading
        fields = [
            'id',                # ID do objeto de leitura de velocidade
            'road_segment',      # ID do segmento (chave estrangeira)
            'average_speed',     # Velocidade média
            'intensity',         # intensidade {elevada/média/baixa}
            'timestamp',         # Data/hora da leitura
            'created_at'         # Data e hora da criação deste objeto na db
        ]
        read_only_fields = ['id', 'created_at']


class RoadSegmentSerializer(serializers.ModelSerializer):
    
    """
    Serializer para o modelo RoadSegment (segmentos de estrada).
    
    Inclui:
    - Todos os campos do segmento
    - total_readings: o número total de leituras feitas
    - latest_reading: a última leitura
    """

    # Estes 2 campos vão ser obtidos através de métodos definidos em baixo
    total_readings = serializers.serializerMethodField()
    latest_reading = serializers.serializerMethodField()

    class Meta:
        model = RoadSegment
        fields = [
              'id',
            'longitude_start',      # Longitude inicial
            'latitude_start',       # Latitude inicial
            'longitude_end',        # Longitude final
            'latitude_end',         # Latitude final
            'length',               # Comprimento do segmento
            'total_readings',       # Número total de leituras deste segmento
            'latest_reading',       # Última leitura deste segmento
            'created_at',           # Timestamp de quando o segemento foi criado
            'updated_at'            # Timestamp de quando o segmento foi modificado
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_total_readings(self, obj):
        
        """
        Devolve o número total de leituras associadas a este segmento.
        
        obj = instância de RoadSegment
        obj.readings = todas as leituras de um determinado segmento
        readings é o related_name que dei quando defini o road_segment como FK
        """
        return obj.readings.count()


    def get_latest_reading(self, obj):
        """
        Devolve a leitura mais recente deste segmento.
        Como a tabela está a ser ordenada do mais recente para o mais antigo então basta fazer: obj.readings.first()
        Se não houver leituras, retorna None.
        """
        latest = obj.readings.first()
        if latest:
            # Serializa o objeto SpeedReading para JSON
            return SpeedReadingSerializer(latest).data
        return None

    


    