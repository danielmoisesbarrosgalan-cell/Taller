from django import forms

from .models import Mecanico


class MecanicoForm(forms.ModelForm):
    """Formulario basado en el modelo ``Mecanico``."""

    class Meta:
        model = Mecanico
        fields = ["nombre", "documento", "telefono", "especialidad", "usuario"]
        labels = {
            "nombre": "Nombre completo",
            "documento": "Documento",
            "telefono": "Teléfono",
            "especialidad": "Especialidad",
            "usuario": "Usuario de acceso (opcional)",
        }
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "documento": forms.TextInput(attrs={"class": "form-control"}),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
            "especialidad": forms.TextInput(attrs={"class": "form-control"}),
            "usuario": forms.Select(attrs={"class": "form-select"}),
        }
