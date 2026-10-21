from django.shortcuts import render


def pagina_no_encontrada(request, exception=None):
    """Renderiza la plantilla personalizada para una URL que no existe."""
    return render(request, "404.html", status=404)
