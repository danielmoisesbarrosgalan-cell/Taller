"""Crea los roles (grupos), usuarios y datos de ejemplo del taller."""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from apps.cliente.models import Cliente
from apps.common.permisos import ADMIN, CLIENTE, MECANICO, RECEPCIONISTA, TODOS
from apps.mecanico.models import Mecanico
from apps.orden.models import DetalleOrden, OrdenServicio
from apps.servicio.models import Servicio
from apps.vehiculo.models import Vehiculo


class Command(BaseCommand):
    help = "Crea grupos, usuarios de prueba y datos de ejemplo."

    def handle(self, *args, **options):
        User = get_user_model()
        grupos = {n: Group.objects.get_or_create(name=n)[0] for n in TODOS}

        def usuario(nombre, clave, rol, **extra):
            u, creado = User.objects.get_or_create(username=nombre, defaults=extra)
            if creado:
                u.set_password(clave)
                u.save()
            u.groups.add(grupos[rol])
            return u

        usuario("admin", "admin123", ADMIN, is_staff=True, is_superuser=True)
        usuario("recepcion", "recepcion123", RECEPCIONISTA)
        u_mec = usuario("mecanico1", "mecanico123", MECANICO)
        u_cli = usuario("cliente1", "cliente123", CLIENTE)

        mecanico, _ = Mecanico.objects.get_or_create(
            documento="1001",
            defaults={"nombre": "Carlos Pérez", "especialidad": "Motor", "usuario": u_mec},
        )
        cliente, _ = Cliente.objects.get_or_create(
            documento="2001",
            defaults={"nombre": "Ana Gómez", "telefono": "3001234567", "usuario": u_cli},
        )
        vehiculo, _ = Vehiculo.objects.get_or_create(
            placa="ABC123",
            defaults={"marca": "Mazda", "modelo": "3", "anio": 2018, "cliente": cliente},
        )
        servicios = [
            ("Cambio de aceite", "Aceite y filtro", 80000),
            ("Alineación y balanceo", "", 60000),
            ("Cambio de frenos", "Pastillas y discos", 150000),
        ]
        for nombre, desc, precio in servicios:
            Servicio.objects.get_or_create(
                nombre=nombre, defaults={"descripcion": desc, "precio_base": precio}
            )

        if not OrdenServicio.objects.exists():
            orden = OrdenServicio.objects.create(
                vehiculo=vehiculo, mecanico=mecanico, problema="Ruido al frenar"
            )
            DetalleOrden.objects.create(
                orden=orden,
                servicio=Servicio.objects.get(nombre="Cambio de frenos"),
                precio=150000,
                observacion="Se cambiaron pastillas delanteras",
            )

        self.stdout.write(self.style.SUCCESS("Datos de ejemplo creados."))
        self.stdout.write(
            "admin/admin123 · recepcion/recepcion123 · "
            "mecanico1/mecanico123 · cliente1/cliente123"
        )
