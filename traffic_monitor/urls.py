from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoadSegmentViewSet, SpeedReadingViewSet

"""
Router do DRF: cria automaticamente os URLs para os ViewSets.

O router trata de criar automaticamente os URLs associados aos ViewSets, sem ser preciso escrever cada endpoint à mão.

Por exemplo:
router.register('segments', RoadSegmentViewSet)

Gera:
- GET    /api/segments/       → RoadSegmentViewSet.list()
- POST   /api/segments/       → RoadSegmentViewSet.create()
- GET    /api/segments/{id}/  → RoadSegmentViewSet.retrieve()
- PUT    /api/segments/{id}/  → RoadSegmentViewSet.update()
- DELETE /api/segments/{id}/  → RoadSegmentViewSet.destroy()
"""

#Começamos por criar o router que vai gerar automaticamente URLs para os ViewSets
router = DefaultRouter()

# Regista os ViewSets no router
# o 1º argumento é o prefixo do URL
# Ex.: 'segments' → /api/segments/
router.register(r'segments', RoadSegmentViewSet, basename='segment')
router.register(r'readings', SpeedReadingViewSet, basename='reading')

# URLs da aplicação
urlpatterns = [
    # Inclui todos os URLs criados pelo router
    path('', include(router.urls)),
]