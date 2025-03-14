from django.contrib import admin
from futbol.models import *
   
from django.contrib.auth.models import User
from futbol.models import Jugador, Equip




class EventInline(admin.TabularInline):
    model = Event
    fields = ["minut", "tipus", "jugador", "equip"]
    ordering = ("minut",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "jugador" and 'object_id' in request.resolver_match.kwargs:
            partit_id = request.resolver_match.kwargs['object_id']
            partit = Partit.objects.get(id=partit_id)
            jugadors_local = [fitxa.jugador.id for fitxa in partit.equip_local.fitxa_set.all()]
            jugadors_visitant = [fitxa.jugador.id for fitxa in partit.equip_visitant.fitxa_set.all()]
            kwargs["queryset"] = Jugador.objects.filter(id__in=jugadors_local + jugadors_visitant)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class PartitAdmin(admin.ModelAdmin):
    list_display = ('equip_local', 'equip_visitant', 'data', 'resultat')
    fields = ('lliga', 'equip_local', 'equip_visitant', 'data', 'gols_local', 'gols_visitant')
    search_fields = ('equip_local__nom__icontains', 'equip_visitant__nom__icontains')
    readonly_fields = ('lliga', 'gols_local', 'gols_visitant')
    inlines = [EventInline]

    def resultat(self, obj):
        gols_local = obj.event_set.filter(tipus_esdeveniment='gol', jugador__equip=obj.equip_local).count()
        gols_visitant = obj.event_set.filter(tipus_esdeveniment='gol', jugador__equip=obj.equip_visitant).count()
        return f"{gols_local} - {gols_visitant}"

    
    def save_model(self, request, obj, form, change):
        obj.gols_local = obj.event_set.filter(tipus=Event.EventType.GOL, equip=obj.equip_local).count()
        obj.gols_visitant = obj.event_set.filter(tipus=Event.EventType.GOL, equip=obj.equip_visitant).count()
        super().save_model(request, obj, form, change)
        



class EquipAdmin(admin.ModelAdmin):
    list_display = ('nom', 'lliga', 'mostrar_usuari')  # Mostrar 'usuari' en el admin
    search_fields = ('nom', 'lliga__nom')  # Buscar por nombre de equipo o liga
    list_filter = ('lliga',)  # Filtros para la liga

    # Método para mostrar el nombre de 'usuari' en el admin
    def mostrar_usuari(self, obj):
        if obj.usuari:
            return obj.usuari.username  # Muestra el nombre del usuario asignado
        return "Sin asignar"
    mostrar_usuari.short_description = 'Gestor'  # Cambiar nombre de la columna en el admin

    # Filtrar por el usuario que está logueado
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:  # Si es superusuario, muestra todos los equipos
            return qs
        return qs.filter(usuari=request.user)  # Si no es superusuario, muestra solo el equipo asignado al usuario




 

class JugadorAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            equip = Equip.objects.get(usuari=request.user)
            return qs.filter(equip=equip)
        except Equip.DoesNotExist:
            return qs.none()
        
        

admin.site.register(Jugador, JugadorAdmin)
admin.site.register(Partit, PartitAdmin)

admin.site.register(Equip, EquipAdmin)
admin.site.register(Lliga)

admin.site.register(Event)
