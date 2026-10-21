from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from apps.common.permisos import ADMIN, rol_requerido

from .forms import ServicioForm
from .models import Servicio

ROLES = (ADMIN,)


@rol_requerido(*ROLES)
def listar_servicios(request):
    """
    Consulta todos los servicios y los envía a la plantilla de listado.

    ``Servicio.objects.all()`` construye un QuerySet (SELECT) que Django
    ejecuta cuando la plantilla lo recorre.
    """
    servicios = Servicio.objects.all()
    return render(request, "servicio/lista_servicios.html", {"servicios": servicios})


@rol_requerido(*ROLES)
def crear_servicio(request):
    """
    Muestra el formulario y guarda un servicio cuando recibe un POST válido.

    ``is_valid()`` aplica las validaciones y ``save()`` ejecuta un INSERT.
    La redirección evita reenviar el formulario al actualizar la página.
    """
    if request.method == "POST":
        form = ServicioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("servicio:lista_servicios")
    else:
        form = ServicioForm()

    contexto = {
        "form": form,
        "titulo": "Crear servicio",
        "texto_boton": "Guardar servicio",
    }
    return render(request, "servicio/crear_servicio.html", contexto)


@rol_requerido(*ROLES)
def editar_servicio(request, id_servicio):
    """
    Actualiza un servicio existente utilizando el mismo formulario.

    Con ``instance`` el ModelForm ejecuta un UPDATE; sin ella crearía un
    registro nuevo.
    """
    servicio = get_object_or_404(Servicio, pk=id_servicio)

    if request.method == "POST":
        form = ServicioForm(request.POST, instance=servicio)
        if form.is_valid():
            form.save()
            return redirect("servicio:lista_servicios")
    else:
        form = ServicioForm(instance=servicio)

    contexto = {
        "form": form,
        "titulo": "Editar servicio",
        "texto_boton": "Actualizar servicio",
    }
    return render(request, "servicio/crear_servicio.html", contexto)


@rol_requerido(*ROLES)
def eliminar_servicio(request, id_servicio):
    """
    Confirma y elimina un servicio.

    En GET solo muestra la confirmación; en POST ejecuta ``delete()``.
    Si tiene registros relacionados (``PROTECT``) se informa al usuario.
    """
    servicio = get_object_or_404(Servicio, pk=id_servicio)

    if request.method == "POST":
        try:
            servicio.delete()
            messages.success(request, "Registro eliminado correctamente.")
        except ProtectedError:
            messages.error(
                request,
                "No se puede eliminar: tiene registros relacionados "
                "(está en órdenes de servicio).",
            )
        return redirect("servicio:lista_servicios")

    contexto = {
        "objeto": servicio,
        "tipo_entidad": "servicio",
        "url_cancelar": reverse("servicio:lista_servicios"),
    }
    return render(request, "confirmar_eliminacion.html", contexto)
