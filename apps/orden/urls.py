from django.urls import path

from . import views

app_name = "orden"

urlpatterns = [
    path("lista/", views.listar_ordenes, name="lista_ordenes"),
    path("crear/", views.crear_orden, name="crear_orden"),
    path("editar/<int:id_orden>/", views.editar_orden, name="editar_orden"),
    path("eliminar/<int:id_orden>/", views.eliminar_orden, name="eliminar_orden"),
    path("detalle/<int:id_orden>/", views.detalle_orden, name="detalle_orden"),
    path("estado/<int:id_orden>/", views.cambiar_estado, name="cambiar_estado"),
    path(
        "detalle/eliminar/<int:id_detalle>/",
        views.eliminar_detalle,
        name="eliminar_detalle",
    ),
]
