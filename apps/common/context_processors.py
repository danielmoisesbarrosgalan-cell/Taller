from .permisos import ADMIN, CLIENTE, MECANICO, RECEPCIONISTA, tiene_rol


def roles(request):
    """Expone el rol del usuario a todas las plantillas."""
    u = request.user
    return {
        "es_admin": tiene_rol(u, ADMIN),
        "es_recepcionista": tiene_rol(u, RECEPCIONISTA),
        "es_mecanico": tiene_rol(u, MECANICO),
        "es_cliente": tiene_rol(u, CLIENTE),
    }
