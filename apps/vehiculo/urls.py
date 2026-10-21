from django.urls import path

from . import views

app_name = "vehiculo"

urlpatterns = [
    path("lista/", views.listar_vehiculos, name="lista_vehiculos"),
    path("crear/", views.crear_vehiculo, name="crear_vehiculo"),
    path("editar/<int:id_vehiculo>/", views.editar_vehiculo, name="editar_vehiculo"),
    path("eliminar/<int:id_vehiculo>/", views.eliminar_vehiculo, name="eliminar_vehiculo"),
]
