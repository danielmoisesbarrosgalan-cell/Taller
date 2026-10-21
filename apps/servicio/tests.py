from django.test import TestCase
from django.urls import reverse

from apps.common.permisos import ADMIN
from apps.common.testing import usuario_con_rol

from .models import Servicio


class ServicioViewsTests(TestCase):
    def setUp(self):
        self.client.force_login(usuario_con_rol(ADMIN))

        self.objeto = Servicio.objects.create(nombre="Cambio de aceite", precio_base=80000)

    def datos(self, **cambios):
        datos = {"nombre": "Alineación", "precio_base": "60000.00"}
        datos.update(cambios)
        return datos

    def test_listar(self):
        response = self.client.get(reverse("servicio:lista_servicios"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "servicio/lista_servicios.html")

    def test_crear(self):
        response = self.client.post(reverse("servicio:crear_servicio"), self.datos())
        self.assertRedirects(response, reverse("servicio:lista_servicios"))
        self.assertTrue(Servicio.objects.filter(nombre="Alineación").exists())

    def test_editar_actualiza_el_mismo_registro(self):
        response = self.client.post(
            reverse("servicio:editar_servicio", args=[self.objeto.pk]),
            self.datos(nombre="Cambio de aceite", precio_base="90000.00"),
        )
        self.assertRedirects(response, reverse("servicio:lista_servicios"))
        self.objeto.refresh_from_db()
        self.assertEqual(self.objeto.precio_base, 90000)

    def test_eliminar(self):
        url = reverse("servicio:eliminar_servicio", args=[self.objeto.pk])
        self.assertEqual(self.client.get(url).status_code, 200)
        self.assertRedirects(self.client.post(url), reverse("servicio:lista_servicios"))
        self.assertFalse(Servicio.objects.filter(pk=self.objeto.pk).exists())

    def test_rol_sin_permiso_recibe_403(self):
        from apps.common.permisos import CLIENTE
        self.client.force_login(usuario_con_rol(CLIENTE))
        response = self.client.get(reverse("servicio:lista_servicios"))
        self.assertEqual(response.status_code, 403)
