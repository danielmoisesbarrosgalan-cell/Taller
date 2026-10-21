from django.urls import path

from . import views

app_name = "cliente"

urlpatterns = [
    path("lista/", views.listar_clientes, name="lista_clientes"),
    path("crear/", views.crear_cliente, name="crear_cliente"),
    path("editar/<int:id_cliente>/", views.editar_cliente, name="editar_cliente"),
    path("eliminar/<int:id_cliente>/", views.eliminar_cliente, name="eliminar_cliente"),
]
