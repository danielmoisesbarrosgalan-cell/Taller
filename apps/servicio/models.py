from django.core.validators import MinValueValidator
from django.db import models

from apps.common.models import ModeloAuditoria


class Servicio(ModeloAuditoria):
    """Catálogo de servicios que ofrece el taller."""

    id_servicio = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=150, unique=True, null=False, blank=False)
    descripcion = models.TextField(null=True, blank=True)
    precio_base = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    class Meta:
        db_table = "servicio"
        ordering = ("nombre",)

    def __str__(self) -> str:
        return self.nombre
