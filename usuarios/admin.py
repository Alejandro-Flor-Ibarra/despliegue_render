from django.contrib import admin
from .models import PagoEntrega, PagoRepartidor, SeguimientoGeolocalizacion

admin.site.register((PagoRepartidor, SeguimientoGeolocalizacion, PagoEntrega))
