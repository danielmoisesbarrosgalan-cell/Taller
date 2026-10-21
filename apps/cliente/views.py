from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from apps.common.permisos import ADMIN, RECEPCIONISTA, rol_requerido

from .forms import ClienteForm
from .models import Cliente

ROLES = (ADMIN, RECEPCIONISTA)


@rol_requerido(*ROLES)
def listar_clientes(request):
    """
    Consulta todos los clientes y los envía a la plantilla de listado.

    ``Cliente.objects.all()`` construye un QuerySet (SELECT) que Django
    ejecuta cuando la plantilla lo recorre.
    """
    clientes = Cliente.objects.all()
    return render(request, "cliente/lista_clientes.html", {"clientes": clientes})


@rol_requerido(*ROLES)
def crear_cliente(request):
    """
    Muestra el formulario y guarda un cliente cuando recibe un POST válido.

    ``is_valid()`` aplica las validaciones y ``save()`` ejecuta un INSERT.
    La redirección evita reenviar el formulario al actualizar la página.
    """
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("cliente:lista_clientes")
    else:
        form = ClienteForm()

    contexto = {
        "form": form,
        "titulo": "Crear cliente",
        "texto_boton": "Guardar cliente",
    }
    return render(request, "cliente/crear_cliente.html", contexto)


@rol_requerido(*ROLES)
def editar_cliente(request, id_cliente):
    """
    Actualiza un cliente existente utilizando el mismo formulario.

    Con ``instance`` el ModelForm ejecuta un UPDATE; sin ella crearía un
    registro nuevo.
    """
    cliente = get_object_or_404(Cliente, pk=id_cliente)

    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect("cliente:lista_clientes")
    else:
        form = ClienteForm(instance=cliente)

    contexto = {
        "form": form,
        "titulo": "Editar cliente",
        "texto_boton": "Actualizar cliente",
    }
    return render(request, "cliente/crear_cliente.html", contexto)


@rol_requerido(*ROLES)
def eliminar_cliente(request, id_cliente):
    """
    Confirma y elimina un cliente.

    En GET solo muestra la confirmación; en POST ejecuta ``delete()``.
    Si tiene registros relacionados (``PROTECT``) se informa al usuario.
    """
    cliente = get_object_or_404(Cliente, pk=id_cliente)

    if request.method == "POST":
        try:
            cliente.delete()
            messages.success(request, "Registro eliminado correctamente.")
        except ProtectedError:
            messages.error(
                request,
                "No se puede eliminar: tiene registros relacionados "
                "(vehículos).",
            )
        return redirect("cliente:lista_clientes")

    contexto = {
        "objeto": cliente,
        "tipo_entidad": "cliente",
        "url_cancelar": reverse("cliente:lista_clientes"),
    }
    return render(request, "confirmar_eliminacion.html", contexto)
