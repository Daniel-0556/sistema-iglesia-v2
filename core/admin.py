from django.contrib import admin
from .models import Iglesia, ConfiguracionSitio, ModoMantenimiento


@admin.register(Iglesia)
class IglesiaAdmin(admin.ModelAdmin):
    list_display = ['nombre_iglesia']


@admin.register(ConfiguracionSitio)
class ConfiguracionSitioAdmin(admin.ModelAdmin):
    list_display = ['nombre_sistema']


@admin.register(ModoMantenimiento)
class ModoMantenimientoAdmin(admin.ModelAdmin):
    list_display = ['activo', 'fecha_actualizacion']