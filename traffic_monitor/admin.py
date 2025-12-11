from django.contrib import admin
from .models import RoadSegment, SpeedReading


@admin.register(RoadSegment)
class RoadSegmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'longitude_start', 'latitude_start', 'length', 'created_at']
    list_filter = ['created_at']
    search_fields = ['id']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(SpeedReading)
class SpeedReadingAdmin(admin.ModelAdmin):
    list_display = ['id', 'road_segment', 'average_speed', 'get_intensity', 'timestamp']    # As colunas da tabela RoadSegment que vão aparecer na página do administrador
    list_filter = ['timestamp', 'road_segment']                                             # Os filtros que o admin tem
    search_fields = ['road_segment__id']                                                    # Barra de pesquisa que permite procurar pelos segmentos através do id
    readonly_fields = ['created_at']                                                        # Campo apenas de leitura, não queremos que seja alterado!!
    
    def get_intensity(self, obj):
        return obj.intensity
    get_intensity.short_description = 'Intensidade'