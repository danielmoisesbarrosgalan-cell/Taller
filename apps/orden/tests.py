from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from apps.cliente.models import Cliente
from apps.common.permisos import ADMIN, CLIENTE, MECANICO, RECEPCIONISTA
from apps.common.testing import usuario_con_rol
from apps.mecanico.models import Mecanico
from apps.servicio.models import Servicio
from apps.vehiculo.models import Vehiculo

from .models import DetalleOrden, OrdenServicio


class OrdenViewsTests(TestCase):
    def setUp(self):
        self.u_mec = usuario_con_rol(MECANICO)
        self.u_cli = usuario_con_rol(CLIENTE)
        self.mecanico = Mecanico.objects.create(
            nombre="Carlos", documento="1001", usuario=self.u_mec
        )
        self.cliente = Cliente.objects.create(
            nombre="Ana", documento="2001", usuario=self.u_cli
        )
        self.vehiculo = Vehiculo.objects.create(
            placa="ABC123", marca="Mazda", modelo="3", cliente=self.cliente
        )
        self.servicio = Servicio.objects.create(
            nombre="Cambio de aceite", precio_base=80000
        )
        self.orden = OrdenServicio.objects.create(
            vehiculo=self.vehiculo, mecanico=self.mecanico, problema="Ruido"
        )
        self.client.force_login(usuario_con_rol(RECEPCIONISTA))

    def test_listar_ordenes(self):
        response = self.client.get(reverse("orden:lista_ordenes"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "orden/lista_ordenes.html")

    def test_crear_orden(self):
        response = self.client.post(
            reverse("orden:crear_orden"),
            {
                "vehiculo": self.vehiculo.pk,
                "mecanico": self.mecanico.pk,
                "estado": "ING",
                "problema": "Revisión general",
            },
        )
        nueva = OrdenServicio.objects.get(problema="Revisión general")
        self.assertRedirects(
            response, reverse("orden:detalle_orden", args=[nueva.pk])
        )

    def test_agregar_servicio_usa_precio_base_si_no_hay_precio(self):
        self.client.post(
            reverse("orden:detalle_orden", args=[self.orden.pk]),
            {"servicio": self.servicio.pk, "precio": "", "observacion": "Sintético"},
        )
        detalle = DetalleOrden.objects.get(orden=self.orden)
        self.assertEqual(detalle.precio, Decimal("80000"))
        self.assertEqual(self.orden.total, Decimal("80000"))

    def test_eliminar_orden_solo_administrador(self):
        url = reverse("orden:eliminar_orden", args=[self.orden.pk])
        self.assertEqual(self.client.get(url).status_code, 403)
        self.client.force_login(usuario_con_rol(ADMIN))
        self.assertRedirects(self.client.post(url), reverse("orden:lista_ordenes"))
        self.assertFalse(OrdenServicio.objects.filter(pk=self.orden.pk).exists())

    def test_mecanico_cambia_estado_de_su_orden(self):
        self.client.force_login(self.u_mec)
        self.client.post(
            reverse("orden:cambiar_estado", args=[self.orden.pk]), {"estado": "REP"}
        )
        self.orden.refresh_from_db()
        self.assertEqual(self.orden.estado, "REP")

    def test_mecanico_no_ve_ordenes_ajenas(self):
        self.client.force_login(usuario_con_rol(MECANICO))
        response = self.client.get(
            reverse("orden:detalle_orden", args=[self.orden.pk])
        )
        self.assertEqual(response.status_code, 404)

    def test_cliente_ve_su_orden_pero_no_puede_editar(self):
        self.client.force_login(self.u_cli)
        url = reverse("orden:detalle_orden", args=[self.orden.pk])
        self.assertEqual(self.client.get(url).status_code, 200)
        response = self.client.post(url, {"servicio": self.servicio.pk})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            self.client.get(reverse("orden:crear_orden")).status_code, 403
        )
