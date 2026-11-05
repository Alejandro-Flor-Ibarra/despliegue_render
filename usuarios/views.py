from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from pymongo.errors import DuplicateKeyError, PyMongoError

from bson.errors import InvalidId
from .forms import (
    PagoEntregaForm,
    PagoRepartidorForm,
    RegistroForm,
    SeguimientoGeolocalizacionForm,
    TipoPagoForm,
)
from .models import PagoEntrega, PagoRepartidor, SeguimientoGeolocalizacion, TipoPago
from .services.mongo_users import (
    buscar_usuario_por_id,
    buscar_usuario_por_nombres,
    crear_usuario,
)


def users(request):
    if request.method == "POST":
        nombres = request.POST.get("username", "").strip()
        contrasena = request.POST.get("password", "")

        try:
            usuario = buscar_usuario_por_nombres(nombres)
        except PyMongoError:
            messages.error(request, "No se pudo conectar con MongoDB.")
            return render(request, "usuarios/users.html")

        if usuario and contrasena == usuario.get("contrasena"):
            request.session["usuario_id"] = str(usuario["_id"])
            return redirect("usuarios:perfil")

        messages.error(request, "Nombre o contraseña incorrectos.")

    return render(request, "usuarios/users.html")


def registro(request):
    form = RegistroForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        try:
            crear_usuario(form.cleaned_data)
        except DuplicateKeyError:
            form.add_error("cedula", "Esa cédula ya está registrada.")
        except PyMongoError:
            form.add_error(
                None,
                "No se pudo conectar con MongoDB. Intenta nuevamente.",
            )
        else:
            messages.success(request, "Usuario registrado correctamente.")
            return redirect("usuarios:login")

    return render(request, "usuarios/registro.html", {"form": form})

def perfil(request):
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        return redirect("usuarios:login")

    try:
        perfil = buscar_usuario_por_id(usuario_id)
    except InvalidId:
        request.session.flush()
        return redirect("users")

    if perfil is None:
        request.session.flush()
        return redirect("usuarios:login")

    return render(request, "usuarios/perfil.html", {"perfil": perfil})


def pagos_repartidor(request):
    form = PagoRepartidorForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pago del repartidor registrado.")
        return redirect("usuarios:pagos_repartidor")

    pagos = PagoRepartidor.objects.order_by("-fecha_pago")
    return render(
        request,
        "usuarios/pagos_repartidor.html",
        {"form": form, "pagos": pagos},
    )


def detalle_pago_repartidor(request, pk):
    pago = get_object_or_404(PagoRepartidor, pk=pk)
    return render(request, "usuarios/detalle_pago_repartidor.html", {"pago": pago})


@require_POST
def eliminar_pago_repartidor(request, pk):
    pago = get_object_or_404(PagoRepartidor, pk=pk)
    pago.delete()
    messages.success(request, "Pago eliminado correctamente.")
    return redirect("usuarios:pagos_repartidor")


def seguimientos(request):
    form = SeguimientoGeolocalizacionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Ubicación registrada.")
        return redirect("usuarios:seguimientos")

    registros = SeguimientoGeolocalizacion.objects.order_by("-timestamp")
    return render(
        request,
        "usuarios/seguimientos.html",
        {"form": form, "seguimientos": registros},
    )


def detalle_seguimiento(request, pk):
    seguimiento = get_object_or_404(SeguimientoGeolocalizacion, pk=pk)
    return render(
        request,
        "usuarios/detalle_seguimiento.html",
        {"seguimiento": seguimiento},
    )


@require_POST
def eliminar_seguimiento(request, pk):
    seguimiento = get_object_or_404(SeguimientoGeolocalizacion, pk=pk)
    seguimiento.delete()
    messages.success(request, "Seguimiento eliminado correctamente.")
    return redirect("usuarios:seguimientos")


def pagos_entrega(request):
    tipo_form = TipoPagoForm()
    pago_form = PagoEntregaForm()

    if request.method == "POST":
        if "btn_tipo_pago" in request.POST:
            tipo_form = TipoPagoForm(request.POST)
            if tipo_form.is_valid():
                tipo_form.save()
                messages.success(request, "Tipo de pago registrado.")
                return redirect("usuarios:pagos_entrega")
        elif "btn_pago_entrega" in request.POST:
            pago_form = PagoEntregaForm(request.POST)
            if pago_form.is_valid():
                pago_form.save()
                messages.success(request, "Pago de entrega registrado.")
                return redirect("usuarios:pagos_entrega")

    return render(
        request,
        "usuarios/pagos_entrega.html",
        {
            "tipo_form": tipo_form,
            "pago_form": pago_form,
            "tipos_pago": TipoPago.objects.all(),
            "pagos": PagoEntrega.objects.select_related("tipo_de_pago"),
        },
    )