from django.contrib import admin
from .models import Equipo

admin.site.register(Equipo)
admin.site.register(lliga)
admin.site.register(Jugador)


class EventInline(admin.TabularInline):
    model = Event
    extra = 2
class PartitAdmin(admin.ModelAdmin):
    inlines = [EventInline]
    
admin.site.register(Partit, PartitAdmin)