from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .models import RoadSegment, SpeedReading
from .serializers import (
    RoadSegmentSerializer, 
    RoadSegmentListSerializer,
    SpeedReadingSerializer)
from .permissions import IsAdminOrReadOnly

@extend_schema_view(
    list=extend_schema(
        summary="Listar todos os segmentos de estrada",
        description="Retorna uma lista de todos os segmentos de estrada, incluindo o número total de leituras associadas.",
        tags=["Segmentos de Estrada"]
    ),
    retrieve=extend_schema(
        summary="Obter detalhes de um segmento",
        description="Retorna os detalhes completos de um segmento específico, incluindo a última leitura e o total de leituras.",
        tags=["Segmentos de Estrada"]
    ),
    create=extend_schema(
        summary="Criar novo segmento (Admin)",
        description="Cria um novo segmento de estrada. Requer autenticação de administrador.",
        tags=["Segmentos de Estrada"]
    ),
    update=extend_schema(
        summary="Atualizar segmento (Admin)",
        description="Atualiza todos os dados de um segmento existente. Requer autenticação de administrador.",
        tags=["Segmentos de Estrada"]
    ),
    partial_update=extend_schema(
        summary="Atualizar parcialmente segmento (Admin)",
        description="Atualiza parcialmente um segmento existente. Requer autenticação de administrador.",
        tags=["Segmentos de Estrada"]
    ),
    destroy=extend_schema(
        summary="Eliminar segmento (Admin)",
        description="Elimina um segmento de estrada. Requer autenticação de administrador.",
        tags=["Segmentos de Estrada"]
    )
)
class RoadSegmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet responsável pela gestão de segmentos de Estrada.
    
    Endpoints criados automaticamente:
    - GET /api/segments/          → Lista todos os segmentos
    - GET /api/segments/{id}/     → Detalhes de um segmento
    - POST /api/segments/         → Criar novo segmento (apenas admin)
    - PUT /api/segments/{id}/     → Editar segmento (apenas admin)
    - DELETE /api/segments/{id}/  → Apagar segmento (apenas admin)
    
    Permissões:
    - Administradores: Podem criar, editar e apagar
    - Utilizadores anónimos: Apenas leitura
    """
    
    # Todos os segmentos existentes na base de dados
    queryset = RoadSegment.objects.all()
    
    # Serializer usado por defeito
    serializer_class = RoadSegmentSerializer
    
    # Permissões aplicadas a este ViewSet
    permission_classes = [IsAdminOrReadOnly]
    
    def get_serializer_class(self):
        """
        Usa serializers diferentes conforme o tipo de pedido
        
        - Listagem → serializer mais simples (menos dados)
        - Detalhe/criação/edição → serializer completo
        """
        if self.action == 'list':
            return RoadSegmentListSerializer
        return RoadSegmentSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Listar leituras de velocidade",
        description="Retorna uma lista de todas as leituras de velocidade. Pode ser filtrada por segmento.",
        parameters=[
            OpenApiParameter(
                name='road_segment',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='ID do segmento para filtrar as leituras',
                required=False
            )
        ],
        tags=["Leituras de Velocidade"]
    ),
    retrieve=extend_schema(
        summary="Obter detalhes de uma leitura",
        description="Retorna os detalhes de uma leitura, incluindo a intensidade calculada.",
        tags=["Leituras de Velocidade"]
    ),
    create=extend_schema(
        summary="Criar nova leitura (Admin)",
        description="Cria uma nova leitura de velocidade associada a um segmento. Requer autenticação de administrador.",
        tags=["Leituras de Velocidade"]
    ),
    update=extend_schema(
        summary="Atualizar leitura (Admin)",
        description="Atualiza todos os dados de uma leitura existente. Requer autenticação de administrador.",
        tags=["Leituras de Velocidade"]
    ),
    partial_update=extend_schema(
        summary="Atualizar parcialmente leitura (Admin)",
        description="Atualiza parcialmente uma leitura existente. Requer autenticação de administrador.",
        tags=["Leituras de Velocidade"]
    ),
    destroy=extend_schema(
        summary="Eliminar leitura (Admin)",
        description="Elimina uma leitura de velocidade. Requer autenticação de administrador.",
        tags=["Leituras de Velocidade"]
    )
)
class SpeedReadingViewSet(viewsets.ModelViewSet):
    """
    ViewSet responsável pelas leituras de Velocidade.
    
    Endpoints criados automaticamente:
    - GET /api/readings/          → Lista todas as leituras
    - GET /api/readings/{id}/     → Detalhes de uma leitura
    - POST /api/readings/         → Criar nova leitura (apenas admin)
    - PUT /api/readings/{id}/     → Editar leitura (apenas admin)
    - DELETE /api/readings/{id}/  → Apagar leitura (apenas admin)
    
    Permissões:
    - Administradores: Podem fazer tudo
    - utilizadores anónimos: Apenas leitura
    """
    
    queryset = SpeedReading.objects.all()
    serializer_class = SpeedReadingSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def get_queryset(self):
        """
        Esta função permite filtrar as leituras pelo segmento de estrada, usando parâmetros no URL.

        Por exemplo: GET /api/readings/?road_segment=1 retorna apenas leituras do segmento 1.
        """
        queryset = super().get_queryset() # SpeedReading.objects.all()
        
        # Obter o ID do segmento passado como parametro na URL
        road_segment_id = self.request.query_params.get('road_segment', None)
        
        if road_segment_id is not None:
            queryset = queryset.filter(road_segment_id=road_segment_id)
        return queryset
