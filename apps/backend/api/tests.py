import os
from unittest.mock import patch

from articles.models import Category
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from sites.models import Site


class InternalAPITests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(username="api-admin", email="admin@example.com", password="local-only")
        self.site = Site.objects.create(name="Signals", domain="localhost", slug="signals")
        self.category = Category.objects.create(site=self.site, name="IA", slug="ia")

    def test_requests_require_internal_token(self):
        with patch.dict(os.environ, {"MCP_INTERNAL_API_TOKEN": "test-token"}):
            response = self.client.get("/api/articles/")
            self.assertEqual(response.status_code, 401)

    def test_authorized_client_can_create_draft(self):
        with patch.dict(os.environ, {"MCP_INTERNAL_API_TOKEN": "test-token"}):
            self.client.credentials(HTTP_AUTHORIZATION="Bearer test-token")
            response = self.client.post("/api/articles/", {"site": self.site.pk, "category": self.category.pk, "title": "Borrador API", "slug": "borrador-api", "excerpt": "Resumen", "content_markdown": "Contenido", "content_type": "signal", "meta_title": "Borrador API", "meta_description": "Descripción"}, format="json")
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.data["state"], "draft")
