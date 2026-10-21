from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.cliente.models import Cliente
from apps.common.models import ModeloAuditoria


class Vehiculo(ModeloAuditoria):
    """Vehículo de un cliente. Relación: Cliente 1:N Vehículo."""

    id_vehiculo = models.BigAutoField(primary_key=True)
    placa = models.CharField(max_length=10, unique=True, null=False, blank=False)
    marca = models.CharField(max_length=60, null=False, blank=False)
    modelo = models.CharField(max_length=60, null=False, blank=False)
    anio = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1900), MaxValueValidator(2100)],
    )
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name="vehiculos",
    )

    class Meta:
        db_table = "vehiculo"
        ordering = ("placa",)
        indexes = [models.Index(fields=["placa"])]

    def __str__(self) -> str:
        return f"{self.placa} - {self.marca} {self.modelo}"
