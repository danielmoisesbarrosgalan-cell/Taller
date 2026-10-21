from django import forms

from .models import Vehiculo


class VehiculoForm(forms.ModelForm):
    """Formulario basado en el modelo ``Vehiculo``."""

    class Meta:
        model = Vehiculo
        fields = ["placa", "marca", "modelo", "anio", "cliente"]
        labels = {
            "placa": "Placa",
            "marca": "Marca",
            "modelo": "Modelo",
            "anio": "Año",
            "cliente": "Propietario",
        }
        widgets = {
            "placa": forms.TextInput(attrs={"class": "form-control", "placeholder": "ABC123"}),
            "marca": forms.TextInput(attrs={"class": "form-control"}),
            "modelo": forms.TextInput(attrs={"class": "form-control"}),
            "anio": forms.NumberInput(attrs={"class": "form-control", "min": "1900", "max": "2100"}),
            "cliente": forms.Select(attrs={"class": "form-select"}),
        }

    def clean_placa(self):
        """Guarda la placa en mayúsculas y sin espacios."""
        return self.cleaned_data["placa"].replace(" ", "").upper()
