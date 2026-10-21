from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from apps.common.permisos import ADMIN, rol_requerido

from .forms import MecanicoForm
from .models import Mecanico

ROLES = (ADMIN,)


@rol_requerido(*ROLES)
def listar_mecanicos(request):
    """
    Consulta todos los mecanicos y los envía a la plantilla de listado.

    ``Mecanico.objects.all()`` construye un QuerySet (SELECT) que Django
    ejecuta cuando la plantilla lo recorre.
    """
    mecanicos = Mecanico.objects.all()
    return render(request, "mecanico/lista_mecanicos.html", {"mecanicos": mecanicos})


@rol_requerido(*ROLES)
def crear_mecanico(request):
    """
    Muestra el formulario y guarda un mecanico cuando recibe un POST válido.

    ``is_valid()`` aplica las validaciones y ``save()`` ejecuta un INSERT.
    La redirección evita reenviar el formulario al actualizar la página.
    """
    if request.method == "POST":
        form = MecanicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("mecanico:lista_mecanicos")
    else:
        form = MecanicoForm()

    contexto = {
        "form": form,
        "titulo": "Crear mecanico",
        "texto_boton": "Guardar mecanico",
    }
    return render(request, "mecanico/crear_mecanico.html", contexto)


@rol_requerido(*ROLES)
def editar_mecanico(request, id_mecanico):
    """
    Actualiza un mecanico existente utilizando el mismo formulario.

    Con ``instance`` el ModelForm ejecuta un UPDATE; sin ella crearía un
    registro nuevo.
    """
    mecanico = get_object_or_404(Mecanico, pk=id_mecanico)

    if request.method == "POST":
        form = MecanicoForm(request.POST, instance=mecanico)
        if form.is_valid():
            form.save()
            return redirect("mecanico:lista_mecanicos")
    else:
        form = MecanicoForm(instance=mecanico)

    contexto = {
        "form": form,
        "titulo": "Editar mecanico",
        "texto_boton": "Actualizar mecanico",
    }
    return render(request, "mecanico/crear_mecanico.html", contexto)


@rol_requerido(*ROLES)
def eliminar_mecanico(request, id_mecanico):
    """
    Confirma y elimina un mecanico.

    En GET solo muestra la confirmación; en POST ejecuta ``delete()``.
    Si tiene registros relacionados (``PROTECT``) se informa al usuario.
    """
    mecanico = get_object_or_404(Mecanico, pk=id_mecanico)

    if request.method == "POST":
        try:
            mecanico.delete()
            messages.success(request, "Registro eliminado correctamente.")
        except ProtectedError:
            messages.error(
                request,
                "No se puede eliminar: tiene registros relacionados "
                "(órdenes asignadas).",
            )
        return redirect("mecanico:lista_mecanicos")

    contexto = {
        "objeto": mecanico,
        "tipo_entidad": "mecanico",
        "url_cancelar": reverse("mecanico:lista_mecanicos"),
    }
    return render(request, "confirmar_eliminacion.html", contexto)
