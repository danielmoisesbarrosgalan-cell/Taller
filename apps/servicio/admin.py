from django.contrib import admin
from .models import Servicio


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ("id_servicio", "nombre", "precio_base")
    search_fields = ("nombre",)
