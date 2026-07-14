from articles.models import Article, Category, Tag
from editorial.models import EditorialGuideline, EditorialTask
from newsletters.models import Edition
from rest_framework import serializers
from sites.models import Site
from sources.models import Source
from trends.models import Trend


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = "__all__"


class EditorialGuidelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = EditorialGuideline
        fields = "__all__"


class EditorialTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = EditorialTask
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at", "completed_at"]


class NewsletterEditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edition
        fields = "__all__"
        read_only_fields = ["created_at", "sent_at"]

    def validate_state(self, value):
        if value not in {"draft", "scheduled"}:
            raise serializers.ValidationError("El API de agentes solo puede crear borradores o programaciones; el envío requiere permisos adicionales.")
        return value


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class TrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trend
        fields = "__all__"


class ArticleSerializer(serializers.ModelSerializer):
    source_ids = serializers.PrimaryKeyRelatedField(source="sources", queryset=Source.objects.all(), many=True, required=False, write_only=True)
    sources = SourceSerializer(many=True, read_only=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=False)

    class Meta:
        model = Article
        fields = ["id", "site", "category", "author", "title", "slug", "excerpt", "content_markdown", "content_type", "tags", "series", "state", "meta_title", "meta_description", "editorial_notes", "impact_score", "maturity_score", "adoption_score", "risk_score", "business_relevance_score", "created_at", "updated_at", "published_at", "sources", "source_ids"]
        read_only_fields = ["created_at", "updated_at", "published_at", "sources"]

    def validate(self, attrs):
        state = attrs.get("state", getattr(self.instance, "state", "draft"))
        if state == "published" and not attrs.get("sources") and not (self.instance and self.instance.sources.exists()):
            raise serializers.ValidationError({"source_ids": "Un artículo publicado debe tener al menos una fuente."})
        return attrs

    def create(self, validated_data):
        sources = validated_data.pop("sources", [])
        article = Article.objects.create(**validated_data)
        article.sources.set(sources)
        return article

    def update(self, instance, validated_data):
        sources = validated_data.pop("sources", None)
        article = super().update(instance, validated_data)
        if sources is not None:
            article.sources.set(sources)
        return article
