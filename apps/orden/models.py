from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from apps.common.models import ModeloAuditoria
from apps.mecanico.models import Mecanico
from apps.servicio.models import Servicio
from apps.vehiculo.models import Vehiculo


class OrdenServicio(ModeloAuditoria):
    """
    Orden que se abre cuando un vehículo ingresa al taller.

    Relaciones: Vehículo 1:N Orden, Mecánico 1:N Orden y
    Orden N:M Servicio mediante ``DetalleOrden``.
    """

    class Estado(models.TextChoices):
        INGRESADO = "ING", "Ingresado"
        EN_REPARACION = "REP", "En reparación"
        TERMINADO = "TER", "Terminado"
        ENTREGADO = "ENT", "Entregado"

    id_orden = models.BigAutoField(primary_key=True)
    fecha_ingreso = models.DateTimeField(default=timezone.now)
    estado = models.CharField(
        max_length=3, choices=Estado.choices, default=Estado.INGRESADO
    )
    problema = models.TextField(null=True, blank=True)

    vehiculo = models.ForeignKey(
        Vehiculo, on_delete=models.PROTECT, related_name="ordenes"
    )
    mecanico = models.ForeignKey(
        Mecanico,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ordenes",
    )
    servicios = models.ManyToManyField(
        Servicio, through="DetalleOrden", related_name="ordenes"
    )

    class Meta:
        db_table = "orden_servicio"
        ordering = ("-fecha_ingreso",)
        indexes = [models.Index(fields=["estado"])]

    def __str__(self) -> str:
        return f"Orden #{self.pk} - {self.vehiculo.placa}"

    @property
    def total(self):
        """Suma de los precios de sus detalles (usa el prefetch si existe)."""
        return sum(d.precio for d in self.detalles.all())


class DetalleOrden(ModeloAuditoria):
    """
    Tabla débil de la relación N:M Orden - Servicio.

    Guarda el precio cobrado y una observación para cada servicio.
    """

    id_detalle = models.BigAutoField(primary_key=True)
    orden = models.ForeignKey(
        OrdenServicio, on_delete=models.CASCADE, related_name="detalles"
    )
    servicio = models.ForeignKey(
        Servicio, on_delete=models.PROTECT, related_name="detalles_orden"
    )
    precio = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    observacion = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "detalle_orden"
        ordering = ("id_detalle",)

    def __str__(self) -> str:
        return f"{self.orden} - {self.servicio} (${self.precio})"
