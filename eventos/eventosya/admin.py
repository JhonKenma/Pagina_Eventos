from django.contrib import admin
from .models import Categoria, Evento, RegistroEvento

# Registro del modelo Categoria
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

# Registro del modelo Evento
@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('nombrEvento', 'fechaInicio', 'fechaFin', 'lugar', 'organizador', 'costo', 'estadoEvento')
    search_fields = ('nombrEvento', 'organizador', 'lugar')
    list_filter = ('categoria', 'estadoEvento')
    ordering = ('fechaInicio',)

# Registro del modelo RegistroEvento
@admin.register(RegistroEvento)
class RegistroEventoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'evento', 'fechaRegistro')
    search_fields = ('usuario__username', 'evento__nombrEvento')
    list_filter = ('fechaRegistro',)
