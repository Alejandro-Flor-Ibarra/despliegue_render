from django import forms

from .models import (
    PagoEntrega,
    PagoRepartidor,
    SeguimientoGeolocalizacion,
    
)


class RegistroForm(forms.Form):
    nombres = forms.CharField(max_length=100)
    apellidos = forms.CharField(max_length=100)
    cedula = forms.CharField(min_length=1, max_length=20)
    edad = forms.IntegerField(min_value=1, max_value=120)
    telefono = forms.CharField(min_length=2, max_length=20)
    contrasena = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput,
    )


class PagoEntregaForm(forms.ModelForm):
    fecha_de_pago = forms.DateTimeField(
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"},
            format="%Y-%m-%dT%H:%M",
        ),
    )

    class Meta:
        model = PagoEntrega
        fields = ["valor_total", "fecha_de_pago", "evidencia_url", "estado"]



class PagoRepartidorForm(forms.ModelForm):
    class Meta:
        model = PagoRepartidor
        fields = [
            "id_repartidor",
            "monto_total_generado",
            "comision_plataforma",
            "monto_neto",
            "estado",
        ]


class SeguimientoGeolocalizacionForm(forms.ModelForm):
    class Meta:
        model = SeguimientoGeolocalizacion
        fields = ["id_repartidor", "latitud", "longitud", "velocidad"]