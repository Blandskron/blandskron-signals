from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError

from .models import Article, ArticleSource, Category, Series, Tag


class ArticleAdminForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = "__all__"

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("state") == "published" and not cleaned.get("sources"):
            raise ValidationError("Un artículo publicado debe tener al menos una fuente.")
        return cleaned


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    list_display = ("title", "content_type", "state", "category", "updated_at")
    list_filter = ("state", "content_type", "site", "category")
    search_fields = ("title", "excerpt", "content_markdown")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
    fieldsets = ((None, {"fields": ("site", "category", "author", "title", "slug", "excerpt", "content_markdown", "content_type", "tags", "series", "state")}), ("SEO", {"fields": ("meta_title", "meta_description")}), ("Índice Blandskron", {"fields": ("impact_score", "maturity_score", "adoption_score", "risk_score", "business_relevance_score", "editorial_notes")}))

    def save_model(self, request, obj, form, change):
        previous_state = ""
        if change:
            previous_state = Article.objects.get(pk=obj.pk).state
        super().save_model(request, obj, form, change)
        if previous_state != obj.state:
            from audit.models import AuditEvent
            AuditEvent.objects.create(actor=request.user, action="article.state_changed", entity_type="article", entity_id=str(obj.pk), previous_state=previous_state, new_state=obj.state, reason=obj.editorial_notes)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "site", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "site", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ("name", "site", "slug")


@admin.register(ArticleSource)
class ArticleSourceAdmin(admin.ModelAdmin):
    list_display = ("article", "source", "added_by_agent")
