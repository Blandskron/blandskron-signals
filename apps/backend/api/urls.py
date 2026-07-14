from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ArticleViewSet,
    CategoryViewSet,
    EditorialTaskViewSet,
    NewsletterEditionViewSet,
    SourceViewSet,
    TagViewSet,
    TrendViewSet,
    content_requirements,
    site_configuration,
)

router = DefaultRouter()
router.register("articles", ArticleViewSet, basename="api-article")
router.register("categories", CategoryViewSet, basename="api-category")
router.register("tags", TagViewSet, basename="api-tag")
router.register("sources", SourceViewSet, basename="api-source")
router.register("trends", TrendViewSet, basename="api-trend")
router.register("editorial-tasks", EditorialTaskViewSet, basename="api-editorial-task")
router.register("newsletter-editions", NewsletterEditionViewSet, basename="api-newsletter-edition")

urlpatterns = [path("", include(router.urls)), path("site-configuration/", site_configuration), path("content-requirements/", content_requirements)]
