from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from apps.common.permisos import (
    ADMIN,
    CLIENTE,
    MECANICO,
    RECEPCIONISTA,
    TODOS,
    rol_requerido,
    tiene_rol,
)

from .forms import DetalleOrdenForm, OrdenServicioForm
from .models import DetalleOrden, OrdenServicio


def ordenes_visibles(usuario):
    """
    Devuelve las órdenes que el usuario puede consultar según su rol.

    Administrador y Recepcionista ven todas; el Mecánico solo las que tiene
    asignadas y el Cliente solo las de sus vehículos.
    """
    ordenes = OrdenServicio.objects.select_related("vehiculo__cliente", "mecanico")
    if tiene_rol(usuario, ADMIN, RECEPCIONISTA):
        return ordenes
    if tiene_rol(usuario, MECANICO):
        return ordenes.filter(mecanico__usuario=usuario)
    if tiene_rol(usuario, CLIENTE):
        return ordenes.filter(vehiculo__cliente__usuario=usuario)
    return ordenes.none()


def puede_gestionar(usuario, orden):
    """Administrador/Recepcionista, o el mecánico asignado a la orden."""
    if tiene_rol(usuario, ADMIN, RECEPCIONISTA):
        return True
    return (
        tiene_rol(usuario, MECANICO)
        and orden.mecanico_id is not None
        and orden.mecanico.usuario_id == usuario.pk
    )


@rol_requerido(*TODOS)
def listar_ordenes(request):
    """
    Lista las órdenes visibles para el usuario.

    ``select_related`` resuelve vehículo, cliente y mecánico con JOIN y
    ``prefetch_related`` carga los detalles para calcular el total sin
    una consulta por fila.
    """
    ordenes = ordenes_visibles(request.user).prefetch_related("detalles")
    return render(request, "orden/lista_ordenes.html", {"ordenes": ordenes})


@rol_requerido(ADMIN, RECEPCIONISTA)
def crear_orden(request):
    """Abre una orden de servicio cuando un vehículo ingresa al taller."""
    if request.method == "POST":
        form = OrdenServicioForm(request.POST)
        if form.is_valid():
            orden = form.save()
            return redirect("orden:detalle_orden", id_orden=orden.pk)
    else:
        form = OrdenServicioForm()

    contexto = {
        "form": form,
        "titulo": "Nueva orden de servicio",
        "texto_boton": "Abrir orden",
    }
    return render(request, "orden/crear_orden.html", contexto)


@rol_requerido(ADMIN, RECEPCIONISTA)
def editar_orden(request, id_orden):
    """Edita vehículo, mecánico, estado y problema de una orden."""
    orden = get_object_or_404(OrdenServicio, pk=id_orden)

    if request.method == "POST":
        form = OrdenServicioForm(request.POST, instance=orden)
        if form.is_valid():
            form.save()
            return redirect("orden:lista_ordenes")
    else:
        form = OrdenServicioForm(instance=orden)

    contexto = {
        "form": form,
        "titulo": f"Editar orden #{orden.pk}",
        "texto_boton": "Actualizar orden",
    }
    return render(request, "orden/crear_orden.html", contexto)


@rol_requerido(ADMIN)
def eliminar_orden(request, id_orden):
    """Confirma y elimina una orden (sus detalles se eliminan en cascada)."""
    orden = get_object_or_404(OrdenServicio, pk=id_orden)

    if request.method == "POST":
        orden.delete()
        messages.success(request, "Orden eliminada correctamente.")
        return redirect("orden:lista_ordenes")

    contexto = {
        "objeto": orden,
        "tipo_entidad": "orden de servicio",
        "url_cancelar": reverse("orden:lista_ordenes"),
    }
    return render(request, "confirmar_eliminacion.html", contexto)


@rol_requerido(*TODOS)
def detalle_orden(request, id_orden):
    """
    Muestra una orden con sus servicios y el total a pagar.

    Quien puede gestionar la orden también agrega servicios desde esta
    página: ``DetalleOrdenForm`` crea la fila de la tabla débil
    ``DetalleOrden`` con su precio y observación.
    """
    orden = get_object_or_404(ordenes_visibles(request.user), pk=id_orden)
    editable = puede_gestionar(request.user, orden)

    if request.method == "POST":
        if not editable:
            raise PermissionDenied
        form = DetalleOrdenForm(request.POST)
        if form.is_valid():
            detalle = form.save(commit=False)
            detalle.orden = orden
            detalle.save()
            return redirect("orden:detalle_orden", id_orden=orden.pk)
    else:
        form = DetalleOrdenForm()

    contexto = {
        "orden": orden,
        "detalles": orden.detalles.select_related("servicio"),
        "form": form,
        "editable": editable,
        "estados": OrdenServicio.Estado.choices,
    }
    return render(request, "orden/detalle_orden.html", contexto)


@rol_requerido(ADMIN, RECEPCIONISTA, MECANICO)
@require_POST
def cambiar_estado(request, id_orden):
    """Cambia el estado de una orden (solo POST)."""
    orden = get_object_or_404(ordenes_visibles(request.user), pk=id_orden)
    if not puede_gestionar(request.user, orden):
        raise PermissionDenied

    nuevo = request.POST.get("estado")
    if nuevo in OrdenServicio.Estado.values:
        orden.estado = nuevo
        orden.save(update_fields=["estado", "actualizado_en"])
        messages.success(request, "Estado actualizado.")
    return redirect("orden:detalle_orden", id_orden=orden.pk)


@rol_requerido(ADMIN, RECEPCIONISTA, MECANICO)
def eliminar_detalle(request, id_detalle):
    """Confirma y quita un servicio de la orden."""
    detalle = get_object_or_404(
        DetalleOrden.objects.select_related("orden", "servicio"), pk=id_detalle
    )
    if not puede_gestionar(request.user, detalle.orden):
        raise PermissionDenied

    url_orden = reverse("orden:detalle_orden", args=[detalle.orden_id])
    if request.method == "POST":
        detalle.delete()
        return redirect(url_orden)

    contexto = {
        "objeto": f"{detalle.servicio} (${detalle.precio})",
        "tipo_entidad": "servicio de la orden",
        "url_cancelar": url_orden,
    }
    return render(request, "confirmar_eliminacion.html", contexto)
