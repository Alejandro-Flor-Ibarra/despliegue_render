from django.shortcuts import render

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .models.repartidores import Pagos_repartidor, Seguimiento_Geolocalizacion


def base_datos(request):
    return render(request, 'base_datos/Bd.html')
def pagos(request):
    lista_pagos = Pagos_repartidor.objects.all()

    return render(
        request,
        'app_PagoRepartidor_SeguimientoGeo/pagos.html',
        {'pagos': lista_pagos},
    )
def seguimientogeo(request):
    lista_seguimientos = Seguimiento_Geolocalizacion.objects.all()

    return render(
        request,
        'app_PagoRepartidor_SeguimientoGeo/SeguimientoGeo.html',
        {'seguimientos': lista_seguimientos},
    )

def detalle_pago(request, id):
    pago = get_object_or_404(Pagos_repartidor, id_pagos=id)

    return render(
        request,
        'app_PagoRepartidor_SeguimientoGeo/detalle_pago.html',
        {'pago': pago},
    )


def eliminar_pago(request, id):
    if request.method == 'POST':
        pago = get_object_or_404(Pagos_repartidor, id_pagos=id)
        pago.delete()
        messages.success(request, 'Pago eliminado correctamente')

    return redirect('pago')


def detalle_seguimiento(request, id):
    seguimiento = get_object_or_404(
        Seguimiento_Geolocalizacion,
        id_Seguimiento=id,
    )

    return render(
        request,
        'app_PagoRepartidor_SeguimientoGeo/detalle_seguimiento.html',
        {'seguimiento': seguimiento},
    )


def eliminar_seguimiento(request, id):
    if request.method == 'POST':
        seguimiento = get_object_or_404(
            Seguimiento_Geolocalizacion,
            id_Seguimiento=id,
        )
        seguimiento.delete()
        messages.success(
            request,
            'Seguimiento eliminado correctamente',
        )

    return redirect('seguimientogeo')