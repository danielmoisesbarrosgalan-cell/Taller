from django.urls import path

from . import views

app_name = "servicio"

urlpatterns = [
    path("lista/", views.listar_servicios, name="lista_servicios"),
    path("crear/", views.crear_servicio, name="crear_servicio"),
    path("editar/<int:id_servicio>/", views.editar_servicio, name="editar_servicio"),
    path("eliminar/<int:id_servicio>/", views.eliminar_servicio, name="eliminar_servicio"),
]
