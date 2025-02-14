from django.contrib import admin

from futbol.models import *



class EventInline(admin.TabularInline):
    model = Event
    extra = 2
class PartitAdmin(admin.ModelAdmin):
    list_display =('equip_local', 'equip_visitant', 'data', 'gols_local', 'gols_visitant')
    fields =('lliga','equip_local', 'equip_visitant', 'data', 'gols_local', 'gols_visitant')
    search_fields = ('equip_local__nom', 'equip_visitant__nom')
    readonly_fields = ('lliga','gols_local', 'gols_visitant')
    inlines = [EventInline]
    
admin.site.register(Equip)
admin.site.register(Lliga)
admin.site.register(Jugador)
admin.site.register(Event)
admin.site.register(Partit, PartitAdmin)

