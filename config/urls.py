from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

"""
URLs principais do projeto.

- /admin/          → Django Admin
- /api/            → API REST (aplicação traffic_monitor)
- /api/docs/       → Documentação Swagger
"""

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),
    
    # API da app traffic_monitor
    # Todos os endpoints começam com /api/
    path('api/', include('traffic_monitor.urls')),
    
    # Documentação da API (Swagger)
    # GET /api/docs/ → Swagger 
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # GET /api/schema/ → Baixa o schema em JSON
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
]