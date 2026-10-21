from django.conf import settings
from django.db import models

from apps.common.models import ModeloAuditoria


class Cliente(ModeloAuditoria):
    """Representa un cliente del taller (tabla ``cliente``)."""

    id_cliente = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=150, null=False, blank=False)
    documento = models.CharField(max_length=20, unique=True, null=False, blank=False)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="perfil_cliente",
        help_text="Usuario con el que el cliente consulta sus órdenes.",
    )

    class Meta:
        db_table = "cliente"
        ordering = ("nombre",)
        indexes = [models.Index(fields=["nombre"])]

    def __str__(self) -> str:
        return self.nombre
