from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Rol, Usuario


admin.site.register(Rol)

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {
            'fields': ('rol', 'iglesia')
        }),
    )