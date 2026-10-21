from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from apps.common.permisos import ADMIN, RECEPCIONISTA, rol_requerido

from .forms import VehiculoForm
from .models import Vehiculo

ROLES = (ADMIN, RECEPCIONISTA)


@rol_requerido(*ROLES)
def listar_vehiculos(request):
    """
    Consulta todos los vehiculos y los envía a la plantilla de listado.

    ``Vehiculo.objects.all()`` construye un QuerySet (SELECT) que Django
    ejecuta cuando la plantilla lo recorre.
    """
    vehiculos = Vehiculo.objects.all().select_related("cliente")
    return render(request, "vehiculo/lista_vehiculos.html", {"vehiculos": vehiculos})


@rol_requerido(*ROLES)
def crear_vehiculo(request):
    """
    Muestra el formulario y guarda un vehiculo cuando recibe un POST válido.

    ``is_valid()`` aplica las validaciones y ``save()`` ejecuta un INSERT.
    La redirección evita reenviar el formulario al actualizar la página.
    """
    if request.method == "POST":
        form = VehiculoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("vehiculo:lista_vehiculos")
    else:
        form = VehiculoForm()

    contexto = {
        "form": form,
        "titulo": "Crear vehiculo",
        "texto_boton": "Guardar vehiculo",
    }
    return render(request, "vehiculo/crear_vehiculo.html", contexto)


@rol_requerido(*ROLES)
def editar_vehiculo(request, id_vehiculo):
    """
    Actualiza un vehiculo existente utilizando el mismo formulario.

    Con ``instance`` el ModelForm ejecuta un UPDATE; sin ella crearía un
    registro nuevo.
    """
    vehiculo = get_object_or_404(Vehiculo, pk=id_vehiculo)

    if request.method == "POST":
        form = VehiculoForm(request.POST, instance=vehiculo)
        if form.is_valid():
            form.save()
            return redirect("vehiculo:lista_vehiculos")
    else:
        form = VehiculoForm(instance=vehiculo)

    contexto = {
        "form": form,
        "titulo": "Editar vehiculo",
        "texto_boton": "Actualizar vehiculo",
    }
    return render(request, "vehiculo/crear_vehiculo.html", contexto)


@rol_requerido(*ROLES)
def eliminar_vehiculo(request, id_vehiculo):
    """
    Confirma y elimina un vehiculo.

    En GET solo muestra la confirmación; en POST ejecuta ``delete()``.
    Si tiene registros relacionados (``PROTECT``) se informa al usuario.
    """
    vehiculo = get_object_or_404(Vehiculo, pk=id_vehiculo)

    if request.method == "POST":
        try:
            vehiculo.delete()
            messages.success(request, "Registro eliminado correctamente.")
        except ProtectedError:
            messages.error(
                request,
                "No se puede eliminar: tiene registros relacionados "
                "(órdenes de servicio).",
            )
        return redirect("vehiculo:lista_vehiculos")

    contexto = {
        "objeto": vehiculo,
        "tipo_entidad": "vehiculo",
        "url_cancelar": reverse("vehiculo:lista_vehiculos"),
    }
    return render(request, "confirmar_eliminacion.html", contexto)
