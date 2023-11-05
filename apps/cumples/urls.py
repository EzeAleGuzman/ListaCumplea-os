from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # Otras URLs de tu aplicación
]
