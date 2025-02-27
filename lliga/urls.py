# lliga/urls.py
from django.contrib import admin
from django.urls import path, include
from futbol import views  # Asegúrate de importar las vistas desde 'futbol'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('futbol/', include('futbol.urls')),
    #path('classificacio/', views.classificacio),  # La vista 'classificacio'
    path("", views.menu, name="menu"),
    path("nou_jugador", views.nou_jugador),
    path("classificacio/<int:lliga_id>", views.classificacio, name="classificacio"),
    path('golejadors/<int:lliga_id>/', views.golejadors, name='golejadors'),  # Nueva ruta
    path('taula_partits/<int:lliga_id>/', views.taula_partits, name='taula_partits'),
]
