from django.test import TestCase
from django.urls import reverse

from apps.common.permisos import ADMIN
from apps.common.testing import usuario_con_rol

from .models import Mecanico


class MecanicoViewsTests(TestCase):
    def setUp(self):
        self.client.force_login(usuario_con_rol(ADMIN))

        self.objeto = Mecanico.objects.create(nombre="Carlos", documento="1001")

    def datos(self, **cambios):
        datos = {"nombre": "Pedro", "documento": "1002", "especialidad": "Frenos"}
        datos.update(cambios)
        return datos

    def test_listar(self):
        response = self.client.get(reverse("mecanico:lista_mecanicos"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mecanico/lista_mecanicos.html")

    def test_crear(self):
        response = self.client.post(reverse("mecanico:crear_mecanico"), self.datos())
        self.assertRedirects(response, reverse("mecanico:lista_mecanicos"))
        self.assertTrue(Mecanico.objects.filter(documento="1002").exists())

    def test_editar_actualiza_el_mismo_registro(self):
        response = self.client.post(
            reverse("mecanico:editar_mecanico", args=[self.objeto.pk]),
            self.datos(nombre="Carlos R.", documento="1001"),
        )
        self.assertRedirects(response, reverse("mecanico:lista_mecanicos"))
        self.objeto.refresh_from_db()
        self.assertEqual(self.objeto.nombre, "Carlos R.")

    def test_eliminar(self):
        url = reverse("mecanico:eliminar_mecanico", args=[self.objeto.pk])
        self.assertEqual(self.client.get(url).status_code, 200)
        self.assertRedirects(self.client.post(url), reverse("mecanico:lista_mecanicos"))
        self.assertFalse(Mecanico.objects.filter(pk=self.objeto.pk).exists())

    def test_rol_sin_permiso_recibe_403(self):
        from apps.common.permisos import CLIENTE
        self.client.force_login(usuario_con_rol(CLIENTE))
        response = self.client.get(reverse("mecanico:lista_mecanicos"))
        self.assertEqual(response.status_code, 403)
