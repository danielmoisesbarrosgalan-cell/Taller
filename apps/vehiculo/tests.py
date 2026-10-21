from django.test import TestCase
from django.urls import reverse

from apps.common.permisos import ADMIN
from apps.common.testing import usuario_con_rol
from apps.cliente.models import Cliente
from .models import Vehiculo


class VehiculoViewsTests(TestCase):
    def setUp(self):
        self.client.force_login(usuario_con_rol(ADMIN))
        self.cliente = Cliente.objects.create(nombre="Ana", documento="2001")
        self.objeto = Vehiculo.objects.create(placa="ABC123", marca="Mazda", modelo="3", anio=2018, cliente=self.cliente)

    def datos(self, **cambios):
        datos = {"placa": "xyz 987", "marca": "Kia", "modelo": "Rio", "anio": 2020, "cliente": self.cliente.pk}
        datos.update(cambios)
        return datos

    def test_listar(self):
        response = self.client.get(reverse("vehiculo:lista_vehiculos"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "vehiculo/lista_vehiculos.html")

    def test_crear(self):
        response = self.client.post(reverse("vehiculo:crear_vehiculo"), self.datos())
        self.assertRedirects(response, reverse("vehiculo:lista_vehiculos"))
        self.assertTrue(Vehiculo.objects.filter(placa="XYZ987").exists())

    def test_editar_actualiza_el_mismo_registro(self):
        response = self.client.post(
            reverse("vehiculo:editar_vehiculo", args=[self.objeto.pk]),
            self.datos(placa="ABC123", marca="Renault"),
        )
        self.assertRedirects(response, reverse("vehiculo:lista_vehiculos"))
        self.objeto.refresh_from_db()
        self.assertEqual(self.objeto.marca, "Renault")

    def test_eliminar(self):
        url = reverse("vehiculo:eliminar_vehiculo", args=[self.objeto.pk])
        self.assertEqual(self.client.get(url).status_code, 200)
        self.assertRedirects(self.client.post(url), reverse("vehiculo:lista_vehiculos"))
        self.assertFalse(Vehiculo.objects.filter(pk=self.objeto.pk).exists())

    def test_rol_sin_permiso_recibe_403(self):
        from apps.common.permisos import CLIENTE
        self.client.force_login(usuario_con_rol(CLIENTE))
        response = self.client.get(reverse("vehiculo:lista_vehiculos"))
        self.assertEqual(response.status_code, 403)
