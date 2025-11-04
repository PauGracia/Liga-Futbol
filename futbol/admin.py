from django.contrib import admin
from .models import Lliga, Equip, Jugador, Partit, Event


# --- INLINE DE EVENTOS DENTRO DE PARTIDOS ---
class EventInline(admin.TabularInline):
    model = Event
    fields = ["minut", "tipus_esdeveniment", "jugador", "mostrar_equip"]
    readonly_fields = ["mostrar_equip"]
    ordering = ("minut",)

    # Mostrar el equipo del jugador
    def mostrar_equip(self, obj):
        return obj.jugador.equip.nom if obj.jugador_id else "-"
    mostrar_equip.short_description = "Equip"

    # Solo mostrar jugadores que pertenezcan a alguno de los equipos del partido
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "jugador" and 'object_id' in request.resolver_match.kwargs:
            partit_id = request.resolver_match.kwargs['object_id']
            partit = Partit.objects.get(id=partit_id)
            jugadors_local = partit.equip_local.jugadors.all()
            jugadors_visitant = partit.equip_visitant.jugadors.all()
            kwargs["queryset"] = jugadors_local | jugadors_visitant
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# --- ADMIN DE PARTITS ---
class PartitAdmin(admin.ModelAdmin):
    list_display = ("lliga", "equip_local", "equip_visitant", "data", "resultat")
    fields = ("lliga", "equip_local", "equip_visitant", "data")
    search_fields = ("equip_local__nom", "equip_visitant__nom")
    list_filter = ("lliga",)
    inlines = [EventInline]

    # Mostrar el resultado de cada partido
    def resultat(self, obj):
        gols_local = obj.event_set.filter(
            tipus_esdeveniment="gol", jugador__equip=obj.equip_local
        ).count()
        gols_visitant = obj.event_set.filter(
            tipus_esdeveniment="gol", jugador__equip=obj.equip_visitant
        ).count()
        return f"{gols_local} - {gols_visitant}"
    resultat.short_description = "Resultat"


# --- ADMIN DE EQUIPS ---
class EquipAdmin(admin.ModelAdmin):
    list_display = ("nom", "lliga", "any_fundacio", "president", "ciutat")
    search_fields = ("nom", "lliga__nom")
    list_filter = ("lliga",)


# --- ADMIN DE JUGADORS ---
class JugadorAdmin(admin.ModelAdmin):
    list_display = ("nom", "equip", "posicio", "dorsal", "nacionalitat", "partits_jugats", "gols_marcats")
    list_filter = ("equip", "posicio", "nacionalitat")
    search_fields = ("nom", "equip__nom")

    def gols_marcats(self, obj):
        return obj.event_set.filter(tipus_esdeveniment="gol").count()
    gols_marcats.short_description = "Gols marcats"


# --- ADMIN DE LLIGUES ---
class LligaAdmin(admin.ModelAdmin):
    list_display = ("nom", "pais")
    search_fields = ("nom", "pais")


# --- ADMIN DE EVENTS ---
class EventAdmin(admin.ModelAdmin):
    list_display = ("partit", "jugador", "tipus_esdeveniment", "minut")
    list_filter = ("tipus_esdeveniment", "partit__lliga")
    search_fields = ("jugador__nom", "partit__equip_local__nom", "partit__equip_visitant__nom")


# --- REGISTROS ---
admin.site.register(Lliga, LligaAdmin)
admin.site.register(Equip, EquipAdmin)
admin.site.register(Jugador, JugadorAdmin)
admin.site.register(Partit, PartitAdmin)
admin.site.register(Event, EventAdmin)
