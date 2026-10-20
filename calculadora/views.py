import json
import math
import re

from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Resultado

# Solo permite números, operadores, punto, paréntesis y espacios
EXPRESION_VALIDA = re.compile(r"^[0-9+\-*/. ()]+$")


def index(request):
    historial = Resultado.objects.all()[:20]
    return render(request, "calculadora/index.html", {"historial": historial})


@require_POST
def guardar(request):
    try:
        datos = json.loads(request.body)
        operacion = str(datos["operacion"])
        resultado = float(datos["resultado"])
    except (ValueError, KeyError, TypeError):
        return JsonResponse({"ok": False}, status=400)

    if (
        len(operacion) > 100
        or not EXPRESION_VALIDA.match(operacion)
        or not math.isfinite(resultado)
    ):
        return JsonResponse({"ok": False}, status=400)

    registro = Resultado.objects.create(operacion=operacion, resultado=resultado)
    return JsonResponse({
        "ok": True,
        "operacion": registro.operacion,
        "resultado": registro.resultado,
        "fecha": timezone.localtime(registro.fecha).strftime("%d/%m/%Y %H:%M:%S"),
    })