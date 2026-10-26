from django.urls import include, path
from . import views

urlpatterns = [
    
    path('', views.base_datos, name='base_datos'),
    path('', include('base_datos.app_PagoRepartidor_SeguimientoGeo.urls')),
    path('', include('base_datos.app_PagosEntrega_TipoPago.urls')),
]