from articles.models import Article, Category, Tag
from audit.models import AuditEvent
from editorial.models import EditorialTask
from newsletters.models import Edition
from rest_framework import filters, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from sites.models import Site
from sources.models import Source
from trends.models import Trend

from .authentication import InternalTokenAuthentication
from .permissions import InternalAPIOnly, RestrictedPublicationPermission
from .serializers import (
    ArticleSerializer,
    CategorySerializer,
    EditorialGuidelineSerializer,
    EditorialTaskSerializer,
    NewsletterEditionSerializer,
    SiteSerializer,
    SourceSerializer,
    TagSerializer,
    TrendSerializer,
)


class SecureViewSet(viewsets.ModelViewSet):
    authentication_classes = [InternalTokenAuthentication]
    permission_classes = [InternalAPIOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]


class ArticleViewSet(SecureViewSet):
    queryset = Article.objects.select_related("site", "category", "author").prefetch_related("tags", "sources")
    serializer_class = ArticleSerializer
    search_fields = ["title", "excerpt", "content_markdown"]
    ordering_fields = ["created_at", "updated_at", "published_at", "title"]

    def get_permissions(self):
        permissions = super().get_permissions()
        if self.action in {"update", "partial_update", "destroy"}:
            permissions.append(RestrictedPublicationPermission())
        return permissions

    def perform_create(self, serializer):
        requested_state = serializer.validated_data.get("state", "draft")
        if requested_state in {"published", "scheduled", "approved"} and not self.request.user.is_superuser:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("La publicación requiere permisos explícitos.")
        article = serializer.save(author=self.request.user, state=requested_state)
        AuditEvent.objects.create(actor=self.request.user, action="article.created_via_api", entity_type="article", entity_id=str(article.pk), new_state=article.state)

    def perform_update(self, serializer):
        previous = serializer.instance.state
        article = serializer.save()
        if previous != article.state:
            AuditEvent.objects.create(actor=self.request.user, action="article.state_changed_via_api", entity_type="article", entity_id=str(article.pk), previous_state=previous, new_state=article.state)


class CategoryViewSet(SecureViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ["name", "slug"]


class TagViewSet(SecureViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    search_fields = ["name", "slug"]


class SourceViewSet(SecureViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    search_fields = ["title", "publisher", "url"]


class TrendViewSet(SecureViewSet):
    queryset = Trend.objects.all()
    serializer_class = TrendSerializer
    search_fields = ["name", "description"]


class EditorialTaskViewSet(SecureViewSet):
    queryset = EditorialTask.objects.select_related("site", "article", "assigned_to")
    serializer_class = EditorialTaskSerializer
    search_fields = ["title", "instructions"]
    filterset_fields = ["state", "task_type", "site"]


class NewsletterEditionViewSet(SecureViewSet):
    queryset = Edition.objects.select_related("campaign", "created_by")
    serializer_class = NewsletterEditionSerializer
    http_method_names = ["get", "post", "patch", "head", "options"]


@api_view(["GET"])
@permission_classes([InternalAPIOnly])
def site_configuration(request):
    site = Site.objects.filter(is_active=True).first()
    if not site:
        return Response({"detail": "No existe un sitio activo."}, status=status.HTTP_404_NOT_FOUND)
    guidelines = getattr(site, "guidelines", None)
    return Response({"site": SiteSerializer(site).data, "guidelines": EditorialGuidelineSerializer(guidelines).data if guidelines else None})


@api_view(["GET"])
@permission_classes([InternalAPIOnly])
def content_requirements(request):
    return Response({"required_for_draft": ["title", "slug", "excerpt", "content_markdown", "content_type", "category", "meta_title", "meta_description"], "required_for_publication": ["sources", "excerpt", "category", "meta_description"], "states": [value for value, _ in Article.STATES]})
