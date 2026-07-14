from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.http import JsonResponse
from django.urls import include, path
from subscribers.views import confirm as subscriber_confirm
from subscribers.views import subscribe, unsubscribe

from .public import (
    ArticleFeed,
    ArticleSitemap,
    article_detail,
    article_list,
    category_detail,
    category_list,
    home,
    text_resource,
    trend_detail,
    trend_list,
)


def health(_request):
    return JsonResponse({"status": "ok", "service": "backend"})


sitemaps = {"articles": ArticleSitemap}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health),
    path("api/", include("api.urls")),
    path("", home, name="home"),
    path("articulos/", article_list, name="article-list"),
    path("articulos/<slug:slug>/", article_detail, name="article-detail"),
    path("categorias/", category_list, name="category-list"),
    path("categorias/<slug:slug>/", category_detail, name="category-detail"),
    path("tendencias/", trend_list, name="trend-list"),
    path("tendencias/<slug:slug>/", trend_detail, name="trend-detail"),
    path("rss.xml", ArticleFeed(), name="rss"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("robots.txt", text_resource, {"resource": "robots.txt"}, name="robots"),
    path("llms.txt", text_resource, {"resource": "llms.txt"}, name="llms"),
    path("llms-full.txt", text_resource, {"resource": "llms-full.txt"}, name="llms-full"),
    path("suscripcion/", subscribe, name="subscribe"),
    path("suscripcion/confirmar/<str:token>/", subscriber_confirm, name="subscriber-confirm"),
    path("suscripcion/cancelar/", unsubscribe, name="subscriber-unsubscribe"),
]
