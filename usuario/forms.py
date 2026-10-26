from django import forms


class RegistroForm(forms.Form):
    nombres = forms.CharField(max_length=100)
    apellidos = forms.CharField(max_length=100)
    cedula = forms.CharField(min_length=5, max_length=20)
    edad = forms.IntegerField(min_value=1, max_value=120)
    telefono = forms.CharField(min_length=7, max_length=20)
    contrasena = forms.CharField(
        min_length=8,
        max_length=128,
        widget=forms.PasswordInput,
    )