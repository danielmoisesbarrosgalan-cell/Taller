"""Utilidades compartidas por las pruebas automatizadas."""

from uuid import uuid4

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


def usuario_con_rol(rol):
    """Crea un usuario y lo agrega al grupo (rol) indicado."""
    usuario = get_user_model().objects.create_user(
        username=f"u_{uuid4().hex[:8]}", password="clave123"
    )
    grupo, _ = Group.objects.get_or_create(name=rol)
    usuario.groups.add(grupo)
    return usuario
