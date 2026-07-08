from django import forms
from .models import Persona, SolicitudEliminacion


class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['nombre_persona', 'telefono_persona']
        widgets = {
            'nombre_persona': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo'
            }),
            'telefono_persona': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 55551234'
            }),
        }
        labels = {
            'nombre_persona': 'Nombre completo',
            'telefono_persona': 'Teléfono',
        }


class SolicitudEliminacionForm(forms.ModelForm):
    class Meta:
        model = SolicitudEliminacion
        fields = ['motivo']
        widgets = {
            'motivo': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Explica brevemente el motivo...'
            }),
        }
        labels = {
            'motivo': 'Motivo de la solicitud',
        }