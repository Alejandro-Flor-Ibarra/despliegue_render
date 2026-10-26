from django.shortcuts import render

def base_datos(request):
    return render(request, 'base_datos/Bd.html')