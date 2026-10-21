from django.urls import path

from . import views

app_name = "mecanico"

urlpatterns = [
    path("lista/", views.listar_mecanicos, name="lista_mecanicos"),
    path("crear/", views.crear_mecanico, name="crear_mecanico"),
    path("editar/<int:id_mecanico>/", views.editar_mecanico, name="editar_mecanico"),
    path("eliminar/<int:id_mecanico>/", views.eliminar_mecanico, name="eliminar_mecanico"),
]
