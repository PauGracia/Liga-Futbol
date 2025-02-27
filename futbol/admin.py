from django.contrib import admin
from futbol.models import *

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
        

admin.site.register(Partit, PartitAdmin)


admin.site.register(Equip)
admin.site.register(Lliga)
admin.site.register(Jugador)
admin.site.register(Event)
