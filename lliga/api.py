
from ninja import NinjaAPI, Schema
from futbol.models import Jugador

api = NinjaAPI()

@api.get("/hello")
def hello(request):
    return "Hello world"


@api.get("/goodbye")
def hello(request):
    return f"Goodbye world"



class JugadorOut(Schema):
    nom: str
    posicio: str
    dorsal: int

@api.get("/jugadors",response=JugadorOut)
def jugadors(request):
    jugador = Jugador.objects.first()
    return jugador
