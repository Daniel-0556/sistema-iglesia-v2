from django.db import models
from core.models import Iglesia
from accounts.models import Usuario


class Persona(models.Model):
    nombre_persona = models.CharField(max_length=200)
    telefono_persona = models.CharField(max_length=20, blank=True)
    iglesia = models.ForeignKey(
        Iglesia,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.nombre_persona

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"


class SolicitudEliminacion(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
    ]
    persona = models.ForeignKey(
        Persona,
        on_delete=models.CASCADE
    )
    solicitada_por = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='solicitudes_enviadas'
    )
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=15,
        choices=ESTADO_CHOICES,
        default='pendiente'
    )
    motivo = models.TextField(blank=True)

    def __str__(self):
        return f"Solicitud: {self.persona} — {self.estado}"

    class Meta:
        verbose_name = "Solicitud de eliminación"
        verbose_name_plural = "Solicitudes de eliminación"