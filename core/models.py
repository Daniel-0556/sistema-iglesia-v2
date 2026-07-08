from django.db import models


class Iglesia(models.Model):
    nombre_iglesia = models.CharField(max_length=200)
    logo = models.ImageField(
        upload_to='logos/',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.nombre_iglesia

    class Meta:
        verbose_name = "Iglesia"
        verbose_name_plural = "Iglesias"


class ConfiguracionSitio(models.Model):
    nombre_sistema = models.CharField(max_length=200, default="Sistema de Asistencias")
    slogan = models.CharField(max_length=300, blank=True)
    color_principal = models.CharField(max_length=7, default="#1a3c6e")
    color_secundario = models.CharField(max_length=7, default="#2a5298")
    logo_sistema = models.ImageField(
        upload_to='sistema/',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.nombre_sistema

    class Meta:
        verbose_name = "Configuración del sitio"
        verbose_name_plural = "Configuración del sitio"


class ModoMantenimiento(models.Model):
    activo = models.BooleanField(default=False)
    mensaje = models.TextField(
        default="Estamos realizando actualizaciones. Por favor vuelve pronto."
    )
    contacto = models.CharField(max_length=200, blank=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Mantenimiento {'ACTIVO' if self.activo else 'INACTIVO'}"

    class Meta:
        verbose_name = "Modo mantenimiento"
        verbose_name_plural = "Modo mantenimiento"