from django.contrib import admin
from .models import Vehiculo


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ("id_vehiculo", "placa", "marca", "modelo", "anio", "cliente")
    list_filter = ("marca",)
    search_fields = ("placa", "cliente__nombre")
