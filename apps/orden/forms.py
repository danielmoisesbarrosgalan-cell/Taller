from django import forms

from apps.vehiculo.models import Vehiculo

from .models import DetalleOrden, OrdenServicio


class OrdenServicioForm(forms.ModelForm):
    """Formulario para abrir y editar órdenes de servicio."""

    class Meta:
        model = OrdenServicio
        fields = ["vehiculo", "mecanico", "estado", "problema"]
        labels = {
            "vehiculo": "Vehículo",
            "mecanico": "Mecánico asignado",
            "estado": "Estado",
            "problema": "Problema reportado",
        }
        widgets = {
            "vehiculo": forms.Select(attrs={"class": "form-select"}),
            "mecanico": forms.Select(attrs={"class": "form-select"}),
            "estado": forms.Select(attrs={"class": "form-select"}),
            "problema": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        """Carga los vehículos con su cliente en un solo JOIN."""
        super().__init__(*args, **kwargs)
        self.fields["vehiculo"].queryset = Vehiculo.objects.select_related("cliente")
        self.fields["vehiculo"].label_from_instance = (
            lambda v: f"{v.placa} - {v.marca} {v.modelo} ({v.cliente})"
        )


class DetalleOrdenForm(forms.ModelForm):
    """
    Agrega un servicio a una orden.

    Si no se escribe un precio, se usa el precio base del servicio.
    """

    class Meta:
        model = DetalleOrden
        fields = ["servicio", "precio", "observacion"]
        labels = {
            "servicio": "Servicio",
            "precio": "Precio (vacío = precio base)",
            "observacion": "Observación",
        }
        widgets = {
            "servicio": forms.Select(attrs={"class": "form-select"}),
            "precio": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
            "observacion": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["precio"].required = False

    def clean(self):
        datos = super().clean()
        servicio = datos.get("servicio")
        if servicio and datos.get("precio") is None:
            datos["precio"] = servicio.precio_base
        return datos
