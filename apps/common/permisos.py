"""
Control de acceso por roles.

Los cuatro actores del sistema son grupos de Django (``Group``):
Administrador, Recepcionista, Mecánico y Cliente. El superusuario se
considera Administrador.
"""

from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

ADMIN = "Administrador"
RECEPCIONISTA = "Recepcionista"
MECANICO = "Mecánico"
CLIENTE = "Cliente"
TODOS = (ADMIN, RECEPCIONISTA, MECANICO, CLIENTE)


def tiene_rol(usuario, *roles):
    """Indica si el usuario pertenece a alguno de los roles indicados."""
    if not usuario.is_authenticated:
        return False
    if usuario.is_superuser:
        return ADMIN in roles
    return usuario.groups.filter(name__in=roles).exists()


def rol_requerido(*roles):
    """
    Decorador para vistas: exige iniciar sesión y pertenecer a un rol.

    Si el usuario no tiene el rol, se lanza ``PermissionDenied`` (HTTP 403).
    """

    def decorador(vista):
        @wraps(vista)
        def envoltura(request, *args, **kwargs):
            if not tiene_rol(request.user, *roles):
                raise PermissionDenied
            return vista(request, *args, **kwargs)

        return login_required(envoltura)

    return decorador
