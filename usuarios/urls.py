from django.urls import path
from . import views

app_name = "usuarios"

urlpatterns = [
    path("", views.users, name="login"),
    path("registro/", views.registro, name="registro"),
    path("perfil/", views.perfil, name="perfil"),


    path("pagos-repartidor/", views.pagos_repartidor, name="pagos_repartidor"),
    path(
        "pagos-repartidor/<int:pk>/",
        views.detalle_pago_repartidor,
        name="detalle_pago_repartidor",
    ),
    path(
        "pagos-repartidor/<int:pk>/eliminar/",
        views.eliminar_pago_repartidor,
        name="eliminar_pago_repartidor",
    ),
    path("seguimientos/", views.seguimientos, name="seguimientos"),
    path(
        "seguimientos/<int:pk>/",
        views.detalle_seguimiento,
        name="detalle_seguimiento",
    ),
    path(
        "seguimientos/<int:pk>/eliminar/",
        views.eliminar_seguimiento,
        name="eliminar_seguimiento",
    ),
    path("pagos-entrega/", views.pagos_entrega, name="pagos_entrega"),
    path(
        "pagos-entrega/nuevo/<str:metodo>/",
        views.nuevo_pago_entrega,
        name="nuevo_pago_entrega",
    ),
]