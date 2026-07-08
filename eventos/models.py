from django.db import models
from core.models import Iglesia
from miembros.models import Persona


class Evento(models.Model):
    tipo_evento = models.CharField(max_length=100)
    fecha_evento = models.DateField()
    iglesia = models.ForeignKey(
        Iglesia,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.tipo_evento} - {self.fecha_evento}"

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"


class Asistencia(models.Model):
    ESTADO_CHOICES = [
        ('presente', 'Presente'),
        ('ausente', 'Ausente'),
        ('justificado', 'Justificado'),
    ]
    evento = models.ForeignKey(
        Evento,
        on_delete=models.CASCADE
    )
    persona = models.ForeignKey(
        Persona,
        on_delete=models.CASCADE
    )
    estado = models.CharField(
        max_length=15,
        choices=ESTADO_CHOICES,
        default='ausente'
    )

    def __str__(self):
        return f"{self.persona} - {self.evento} - {self.estado}"

    class Meta:
        verbose_name = "Asistencia"
        verbose_name_plural = "Asistencias"