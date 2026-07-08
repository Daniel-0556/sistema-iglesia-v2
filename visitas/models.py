from django.db import models
from miembros.models import Persona
from accounts.models import Usuario


class VisitaPendiente(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('realizada', 'Realizada'),
    ]
    persona = models.ForeignKey(
        Persona,
        on_delete=models.CASCADE,
        related_name='visitas'
    )
    creada_por = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        related_name='visitas_creadas'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=15,
        choices=ESTADO_CHOICES,
        default='pendiente'
    )
    notas = models.TextField(blank=True)
    fecha_realizada = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Visita {self.estado}: {self.persona.nombre_persona}"

    class Meta:
        verbose_name = "Visita"
        verbose_name_plural = "Visitas"