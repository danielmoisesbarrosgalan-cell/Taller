from django.contrib import admin
from .models import Mecanico


@admin.register(Mecanico)
class MecanicoAdmin(admin.ModelAdmin):
    list_display = ("id_mecanico", "nombre", "documento", "especialidad")
    search_fields = ("nombre", "documento")
