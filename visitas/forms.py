from django import forms
from .models import VisitaPendiente


class VisitaRealizadaForm(forms.ModelForm):
    class Meta:
        model = VisitaPendiente
        fields = ['notas']
        widgets = {
            'notas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Escribe aquí las notas de la visita realizada...'
            }),
        }
        labels = {
            'notas': 'Notas de la visita',
        }