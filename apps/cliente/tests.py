from django.test import TestCase
from django.urls import reverse

from apps.common.permisos import ADMIN
from apps.common.testing import usuario_con_rol

from .models import Cliente


class ClienteViewsTests(TestCase):
    def setUp(self):
        self.client.force_login(usuario_con_rol(ADMIN))

        self.objeto = Cliente.objects.create(nombre="Ana Gómez", documento="2001")

    def datos(self, **cambios):
        datos = {"nombre": "Luis Mora", "documento": "3001", "telefono": "300"}
        datos.update(cambios)
        return datos

    def test_listar(self):
        response = self.client.get(reverse("cliente:lista_clientes"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cliente/lista_clientes.html")

    def test_crear(self):
        response = self.client.post(reverse("cliente:crear_cliente"), self.datos())
        self.assertRedirects(response, reverse("cliente:lista_clientes"))
        self.assertTrue(Cliente.objects.filter(documento="3001").exists())

    def test_editar_actualiza_el_mismo_registro(self):
        response = self.client.post(
            reverse("cliente:editar_cliente", args=[self.objeto.pk]),
            self.datos(nombre="Ana Actualizada", documento="2001"),
        )
        self.assertRedirects(response, reverse("cliente:lista_clientes"))
        self.objeto.refresh_from_db()
        self.assertEqual(self.objeto.nombre, "Ana Actualizada")

    def test_eliminar(self):
        url = reverse("cliente:eliminar_cliente", args=[self.objeto.pk])
        self.assertEqual(self.client.get(url).status_code, 200)
        self.assertRedirects(self.client.post(url), reverse("cliente:lista_clientes"))
        self.assertFalse(Cliente.objects.filter(pk=self.objeto.pk).exists())

    def test_rol_sin_permiso_recibe_403(self):
        from apps.common.permisos import CLIENTE
        self.client.force_login(usuario_con_rol(CLIENTE))
        response = self.client.get(reverse("cliente:lista_clientes"))
        self.assertEqual(response.status_code, 403)
