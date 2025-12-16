from rest_framework import serializers
from .models import RoadSegment, SpeedReading


class SpeedReadingSerializer(serializers.ModelSerializer):

    """
    Serializer para leituras de velocidade.
    
    Responsável por Converter objetos SpeedReading em JSON e vice-versa.
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
    Serializer do segmentos de estrada.
    
    Para além dos campos do modelo, inclui também:
    - total_readings: número de leituras associadas
    - latest_reading: a leitura mais recente
    """

    total_readings = serializers.SerializerMethodField()
    latest_reading = serializers.SerializerMethodField()

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
        """
        return obj.readings.count()


    def get_latest_reading(self, obj):
        """
        Devolve a leitura mais recente deste segmento.
        Se não existirem leituras, retorna None.
        """
        latest = obj.readings.first()
        if latest:
            # Serializa o objeto SpeedReading para JSON
            return SpeedReadingSerializer(latest).data
        return None


class RoadSegmentListSerializer(serializers.ModelSerializer):
    """
    Serializer + simples para facilitar a listagem de segmentos.
    
    Será utilizado no endpoint GET /api/segments/ (lista)
    Não inclui latest_reading para reduzir a quantidade de dados a serem devolvidos.
    """
    total_readings = serializers.SerializerMethodField()
    
    class Meta:
        model = RoadSegment
        fields = [
            'id',
            'longitude_start',
            'latitude_start',
            'longitude_end',
            'latitude_end',
            'length',
            'total_readings'
        ]
    
    def get_total_readings(self, obj):
        """
        Devolve o número de leituras de velocidade do segmento.
        """
        return obj.readings.count()