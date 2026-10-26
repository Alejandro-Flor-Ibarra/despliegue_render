from django.urls import path

from . import views

urlpatterns = [
    path('pago/', views.pagos, name='pago'),
    path(
        'pago/<int:id>/',
        views.detalle_pago,
        name='detalle_pago',
    ),
    path(
        'pago/<int:id>/eliminar/',
        views.eliminar_pago,
        name='eliminar_pago',
    ),

    path(
        'seguimientogeo/',
        views.seguimientogeo,
        name='seguimientogeo',
    ),
    path(
        'seguimientogeo/<int:id>/',
        views.detalle_seguimiento,
        name='detalle_seguimiento',
    ),
    path(
        'seguimientogeo/<int:id>/eliminar/',
        views.eliminar_seguimiento,
        name='eliminar_seguimiento',
    ),
]