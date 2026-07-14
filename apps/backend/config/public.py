from articles.models import Article, Category
from django.contrib.sitemaps import Sitemap
from django.contrib.syndication.views import Feed
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from trends.models import Trend


def published_articles():
    return Article.objects.filter(state="published").select_related("site", "category", "author").prefetch_related("tags", "sources")


def home(request):
    articles = published_articles()
    return render(request, "home.html", {"featured": articles.first(), "articles": articles[1:7], "trends": Trend.objects.order_by("-updated_at")[:6]})


def article_list(request):
    articles = published_articles()
    query = request.GET.get("q", "").strip()
    if query:
        articles = articles.filter(Q(title__icontains=query) | Q(excerpt__icontains=query) | Q(content_markdown__icontains=query))
    return render(request, "articles/list.html", {"articles": articles, "query": query})


def article_detail(request, slug):
    article = get_object_or_404(published_articles(), slug=slug)
    related = published_articles().filter(category=article.category).exclude(pk=article.pk)[:3]
    return render(request, "articles/detail.html", {"article": article, "related": related})


def category_list(request):
    return render(request, "categories/list.html", {"categories": Category.objects.order_by("name")})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    return render(request, "categories/detail.html", {"category": category, "articles": published_articles().filter(category=category)})


def trend_list(request):
    return render(request, "trends/list.html", {"trends": Trend.objects.order_by("category", "-updated_at")})


def trend_detail(request, slug):
    trend = get_object_or_404(Trend, slug=slug)
    return render(request, "trends/detail.html", {"trend": trend, "articles": published_articles().filter(title__icontains=trend.name)[:5]})


def text_resource(request, resource):
    content = {
        "llms.txt": "# Blandskron Signals\n\nObservatorio tecnológico editorial en español sobre IA, software, agentes, automatización, infraestructura y ciberseguridad.\n\nConsulta el RSS en /rss.xml y el sitemap en /sitemap.xml. Cita cada artículo con su título, URL y fecha de actualización.\n",
        "llms-full.txt": "# Blandskron Signals\n\nPublicación tecnológica independiente con Signals, Analysis, Field Notes, Radar, Living Articles y Briefings. Las fuentes visibles en cada artículo forman parte del registro editorial.\n\nPolítica: distinguimos hechos, interpretación y opinión; priorizamos documentación oficial y fuentes primarias; no aceptamos contenido sin fuentes verificables.\n",
        "robots.txt": "User-agent: *\nAllow: /\nDisallow: /admin/\nSitemap: /sitemap.xml\n",
    }
    return HttpResponse(content[resource], content_type="text/plain; charset=utf-8")


class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return published_articles()

    def location(self, item):
        return reverse("article-detail", kwargs={"slug": item.slug})

    def lastmod(self, item):
        return item.updated_at


class ArticleFeed(Feed):
    title = "Blandskron Signals"
    description = "Señales, análisis y notas sobre tecnología."
    link = "/articulos/"

    def items(self):
        return published_articles()[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.excerpt

    def item_link(self, item):
        return reverse("article-detail", kwargs={"slug": item.slug})

    def item_pubdate(self, item):
        return item.published_at or item.updated_at
