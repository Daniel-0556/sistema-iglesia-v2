from django import forms
from .models import Evento


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['tipo_evento', 'fecha_evento']
        widgets = {
            'tipo_evento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Culto dominical, Reunión de jóvenes...'
            }),
            'fecha_evento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
        labels = {
            'tipo_evento': 'Tipo de evento',
            'fecha_evento': 'Fecha',
        }