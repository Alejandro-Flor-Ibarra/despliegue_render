from django.shortcuts import render

def home(request):
    return render(request, 'home/home.html')


def terms(request):
    return render(request, 'home/terms.html')