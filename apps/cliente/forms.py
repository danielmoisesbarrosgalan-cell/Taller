from django import forms

from .models import Cliente


class ClienteForm(forms.ModelForm):
    """Formulario basado en el modelo ``Cliente``."""

    class Meta:
        model = Cliente
        fields = ["nombre", "documento", "telefono", "email", "usuario"]
        labels = {
            "nombre": "Nombre completo",
            "documento": "Documento",
            "telefono": "Teléfono",
            "email": "Correo electrónico",
            "usuario": "Usuario de acceso (opcional)",
        }
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Escriba el nombre"}),
            "documento": forms.TextInput(attrs={"class": "form-control"}),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "usuario": forms.Select(attrs={"class": "form-select"}),
        }
