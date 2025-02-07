# futbol/views.py
from django.http import HttpResponse

def equipos(request):
    return HttpResponse("Aquí están los equipos de fútbol")
