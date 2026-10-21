"""Rutas principales del proyecto Taller Mecánico."""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path, re_path
from django.views.generic import TemplateView

from apps.common.views import pagina_no_encontrada

handler404 = "apps.common.views.pagina_no_encontrada"

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("cliente/", include("apps.cliente.urls")),
    path("vehiculo/", include("apps.vehiculo.urls")),
    path("mecanico/", include("apps.mecanico.urls")),
    path("servicio/", include("apps.servicio.urls")),
    path("orden/", include("apps.orden.urls")),
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
]

urlpatterns += [
    re_path(r"^.*$", pagina_no_encontrada, name="pagina_no_encontrada"),
]
