from django.urls import path
from . import views

urlpatterns = [
    path('', views.users, name='users'),
    path('users/', views.users, name='users'),
    path('registro/', views.registro, name='registro'),
    path('perfil/', views.perfil, name='perfil'),
]