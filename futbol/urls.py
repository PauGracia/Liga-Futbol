# futbol/urls.py
from django.urls import path
from . import views  # Importa las vistas de la misma app

urlpatterns = [
    path('classificacio/', views.classificacio, name='classificacio'),  # Vista para la clasificación
]



