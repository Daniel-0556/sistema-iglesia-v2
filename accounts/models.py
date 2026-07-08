from django.db import models
from django.contrib.auth.models import AbstractUser


class Rol(models.Model):
    nombre_rol = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre_rol

    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"


class Usuario(AbstractUser):
    rol = models.ForeignKey(
        Rol,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    iglesia = models.ForeignKey(
        'core.Iglesia',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
