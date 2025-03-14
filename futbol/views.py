from django.shortcuts import render
from django import forms
from futbol.models import *
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
    

    
class MenuForm(forms.Form):
    lliga = forms.ModelChoiceField(queryset=Lliga.objects.all())
    
class JugadorForm(forms.ModelForm):
    class Meta:
        model = Jugador
        fields = "__all__"

def nou_jugador(request):
    if request.method == "POST":
        form = JugadorForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el nuevo jugador en la base de datos
            return redirect('menu')  # Redirige a la página principal o a donde desees
    else:
        form = JugadorForm()  # Si es GET, muestra el formulario vacío

    return render(request, "nou_jugador.html", {"form": form})

    
    
    
def menu(request):
    form = MenuForm()
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            lliga = form.cleaned_data.get("lliga")
            # cridem a /classificacio/<lliga_id>
            return redirect('classificacio',lliga.id)
    return render(request, "menu.html",{
                    "form": form,
            })

# Función para mostrar la classificación de golejadors
def golejadors(request, lliga_id):
    lliga = Lliga.objects.get(id=lliga_id)
    
    # Obtener todos los partidos de la liga
    partits = lliga.partits.all()
    
    # Obtener todos los eventos de tipo "gol" en esos partidos
    gols = Event.objects.filter(partit__in=partits, tipus_esdeveniment="gol")
    
    # Contar goles por jugador
    golejadors = {}
    for gol in gols:
        jugador = gol.jugador
        if jugador in golejadors:
            golejadors[jugador] += 1
        else:
            golejadors[jugador] = 1
    
    # Convertir el diccionario en lista y ordenar por goles (de mayor a menor)
    classificacio_golejadors = sorted(golejadors.items(), key=lambda x: x[1], reverse=True)
    
    return render(request, "golejadors.html", {
        "lliga": lliga,
        "classificacio_golejadors": classificacio_golejadors
    })


# Función para mostrar la taula de partits
def taula_partits(request, lliga_id):
    lliga = Lliga.objects.get(id=lliga_id)
    equips = list(lliga.equips.all())  # Obtener todos los equipos de la liga

    # Crear la estructura de la tabla
    resultats = [[""] + [equip.nom for equip in equips]]  # Primera fila (encabezado)

    for equip1 in equips:
        fila = [equip1.nom]  # Primera columna (nombre del equipo)

        for equip2 in equips:
            if equip1 == equip2:
                fila.append("X")  # Si es el mismo equipo, ponemos una "X"
            else:
                # Buscar el partido entre equip1 y equip2
                partit = Partit.objects.filter(
                    lliga=lliga,
                    equip_local=equip1,
                    equip_visitant=equip2
                ).first()

                if partit:
                    resultat = f"{partit.gols_local()} - {partit.gols_visitant()}"
                else:
                    resultat = "-"

                fila.append(resultat)  # Añadir el resultado o un guion si no hay partido
        
        resultats.append(fila)  # Agregar la fila a la tabla

    return render(request, "taula_partits.html", {"resultats": resultats, "lliga": lliga})




def classificacio(request, lliga_id):
    lliga = Lliga.objects.get(id=lliga_id)
    equips = lliga.equips.all()
    classi = []
    
    # Calcular punts per a cada equip
    for equip in equips:
        punts = 0
        
        # Calcular punts per partits locals
        for partit in lliga.partits.filter(equip_local=equip):
            gols_local = partit.gols_local()
            gols_visitant = partit.gols_visitant()
            if gols_local > gols_visitant:
                punts += 3
            elif gols_local == gols_visitant:
                punts += 1
        
        # Calcular punts per partits visitants
        for partit in lliga.partits.filter(equip_visitant=equip):
            gols_local = partit.gols_local()
            gols_visitant = partit.gols_visitant()
            if gols_local < gols_visitant:
                punts += 3
            elif gols_local == gols_visitant:
                punts += 1
        
        # Afegim l'equip i els seus punts a la llista
        classi.append((punts, equip.nom))
    
    # Ordenem la llista de forma descendent
    classi.sort(reverse=True, key=lambda x: x[0])  # Ordenar per punts
    
    #return render(request, "classificacio.html", {"classificacio": classi})
    return render(request, "classificacio.html", {"classificacio": classi, "lliga": lliga})






@login_required
def gestionar_equip(request):
    try:
        equip = Equip.objects.get(usuari=request.user)
    except Equip.DoesNotExist:
        return render(request, "error.html", {"error": "No tienes un equipo asignado."})

    jugadors = equip.jugadors.all()

    return render(request, "gestionar_equip.html", {"equip": equip, "jugadors": jugadors})




