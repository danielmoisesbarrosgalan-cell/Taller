from django.contrib import admin
from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("id_cliente", "nombre", "documento", "telefono", "email")
    search_fields = ("nombre", "documento")
