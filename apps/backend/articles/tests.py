from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from sites.models import Site
from sources.models import Source

from .models import Article, Category


class ArticleEditorialTests(TestCase):
    def setUp(self):
        self.site = Site.objects.create(name="Blandskron Signals", domain="localhost", slug="blandskron-signals")
        self.category = Category.objects.create(site=self.site, name="IA", slug="ia")
        self.source = Source.objects.create(title="Documentación oficial", url="https://example.com/docs", publisher="Example", source_type="official")
        self.article = Article.objects.create(site=self.site, category=self.category, author=get_user_model().objects.create_user(username="editor"), title="Señal", slug="senal", excerpt="Resumen", content_markdown="Contenido", meta_description="Descripción")

    def test_published_article_requires_source(self):
        self.article.state = "published"
        with self.assertRaises(ValidationError):
            self.article.full_clean()

    def test_article_can_be_published_with_source(self):
        self.article.sources.add(self.source)
        self.article.state = "published"
        self.article.full_clean()
