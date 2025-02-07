from django.contrib import admin
from django.urls import path, include  # Importa 'include' para incluir las urls de la app 'futbol'

urlpatterns = [
    path('admin/', admin.site.urls),
]
