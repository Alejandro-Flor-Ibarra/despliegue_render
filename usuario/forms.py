from django import forms


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