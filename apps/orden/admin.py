from django.contrib import admin
from .models import DetalleOrden, OrdenServicio


class DetalleOrdenInline(admin.TabularInline):
    model = DetalleOrden
    extra = 1


@admin.register(OrdenServicio)
class OrdenServicioAdmin(admin.ModelAdmin):
    list_display = ("id_orden", "fecha_ingreso", "vehiculo", "mecanico", "estado")
    list_filter = ("estado", "mecanico")
    search_fields = ("vehiculo__placa", "vehiculo__cliente__nombre")
    inlines = [DetalleOrdenInline]


@admin.register(DetalleOrden)
class DetalleOrdenAdmin(admin.ModelAdmin):
    list_display = ("id_detalle", "orden", "servicio", "precio")
