from django.contrib import messages
from django.shortcuts import redirect, render
from pymongo.errors import DuplicateKeyError, PyMongoError

from .forms import RegistroForm
from .services.mongo_users import crear_usuario

from bson.errors import InvalidId
from .services.mongo_users import buscar_usuario_por_id



def users(request):
    return render(request, "usuario/users.html")


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
            return redirect("users")

    return render(request, "usuario/registro.html", {"form": form})

def perfil(request):
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        return redirect("users")

    try:
        perfil = buscar_usuario_por_id(usuario_id)
    except InvalidId:
        request.session.flush()
        return redirect("users")

    if perfil is None:
        request.session.flush()
        return redirect("users")

    return render(request, "usuario/perfil.html", {"perfil": perfil})