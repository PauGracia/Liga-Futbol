from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu, name='menu'),
    path('classificacio/<int:lliga_id>/', views.classificacio, name='classificacio'),
    path('jugador/<int:jugador_id>/', views.jugador_detall, name='jugador_detall'),
    path('golejadors/<int:lliga_id>/', views.golejadors, name='golejadors'),
    path('taula_partits/<int:lliga_id>/', views.taula_partits, name='taula_partits'),
    path('equip/<int:equip_id>/', views.equip_detall, name='equip_detall'),
    path('classificacio_porters/<int:lliga_id>/', views.classificacio_porters, name='classificacio_porters'),
]
