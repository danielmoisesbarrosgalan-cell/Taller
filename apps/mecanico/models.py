from django.conf import settings
from django.db import models

from apps.common.models import ModeloAuditoria


class Mecanico(ModeloAuditoria):
    """Mecánico del taller (tabla ``mecanico``)."""

    id_mecanico = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=150, null=False, blank=False)
    documento = models.CharField(max_length=20, unique=True, null=False, blank=False)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    especialidad = models.CharField(max_length=100, null=True, blank=True)
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="perfil_mecanico",
        help_text="Usuario con el que el mecánico ve sus órdenes.",
    )

    class Meta:
        db_table = "mecanico"
        ordering = ("nombre",)

    def __str__(self) -> str:
        return self.nombre
