from django import forms

from .models import Servicio


class ServicioForm(forms.ModelForm):
    """Formulario basado en el modelo ``Servicio``."""

    class Meta:
        model = Servicio
        fields = ["nombre", "descripcion", "precio_base"]
        labels = {
            "nombre": "Nombre del servicio",
            "descripcion": "Descripción",
            "precio_base": "Precio base",
        }
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "precio_base": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
        }
