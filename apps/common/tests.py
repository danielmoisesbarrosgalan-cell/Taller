from django.test import TestCase
from django.urls import reverse


class PaginasBasicasTests(TestCase):
    def test_inicio_es_publico(self):
        self.assertEqual(self.client.get(reverse("index")).status_code, 200)

    def test_url_inexistente_responde_404(self):
        response = self.client.get("/ruta/que/no/existe/")
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")

    def test_vistas_exigen_login(self):
        response = self.client.get(reverse("cliente:lista_clientes"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
