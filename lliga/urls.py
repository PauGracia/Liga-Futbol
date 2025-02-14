from django.contrib import admin
from django.urls import path, include  # Importa 'include' para incluir las urls de la app 'futbol'
from futbol import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('classificacio/', views.classificacio),
    
]




