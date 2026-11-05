from django.contrib import admin
from .models import PagoEntrega, PagoRepartidor, SeguimientoGeolocalizacion, TipoPago

admin.site.register((PagoRepartidor, SeguimientoGeolocalizacion, TipoPago, PagoEntrega))
