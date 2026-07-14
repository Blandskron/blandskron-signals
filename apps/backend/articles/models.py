from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    site = models.ForeignKey("sites.Site", on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=120)
    slug = models.SlugField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["site", "slug"], name="unique_category_slug_per_site")]
        ordering = ["name"]

    def __str__(self):
        return self.name


class Tag(models.Model):
    site = models.ForeignKey("sites.Site", on_delete=models.CASCADE, related_name="tags")
    name = models.CharField(max_length=80)
    slug = models.SlugField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["site", "slug"], name="unique_tag_slug_per_site")]
        ordering = ["name"]

    def __str__(self):
        return self.name


class Series(models.Model):
    site = models.ForeignKey("sites.Site", on_delete=models.CASCADE, related_name="series")
    name = models.CharField(max_length=160)
    slug = models.SlugField()
    description = models.TextField(blank=True)


class Article(models.Model):
    CONTENT_TYPES = [(value, value.replace("_", " ").title()) for value in ("signal", "analysis", "field_note", "radar", "living_article", "briefing")]
    STATES = [(value, value.title()) for value in ("idea", "researching", "draft", "review", "approved", "scheduled", "published", "archived", "rejected")]
    site = models.ForeignKey("sites.Site", on_delete=models.PROTECT, related_name="articles")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="articles")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="articles")
    title = models.CharField(max_length=240)
    slug = models.SlugField(max_length=260)
    excerpt = models.TextField()
    content_markdown = models.TextField()
    content_type = models.CharField(max_length=24, choices=CONTENT_TYPES, default="signal")
    tags = models.ManyToManyField(Tag, blank=True, related_name="articles")
    series = models.ForeignKey(Series, null=True, blank=True, on_delete=models.SET_NULL, related_name="articles")
    state = models.CharField(max_length=20, choices=STATES, default="idea")
    meta_title = models.CharField(max_length=240, blank=True)
    meta_description = models.CharField(max_length=320, blank=True)
    editorial_notes = models.TextField(blank=True)
    impact_score = models.PositiveSmallIntegerField(default=0)
    maturity_score = models.PositiveSmallIntegerField(default=0)
    adoption_score = models.PositiveSmallIntegerField(default=0)
    risk_score = models.PositiveSmallIntegerField(default=0)
    business_relevance_score = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    sources = models.ManyToManyField("sources.Source", through="ArticleSource", related_name="articles")

    class Meta:
        constraints = [models.UniqueConstraint(fields=["site", "slug"], name="unique_article_slug_per_site")]
        ordering = ["-published_at", "-created_at"]

    def clean(self):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        if self.state == "published":
            missing = []
            if not self.meta_description:
                missing.append("meta_description")
            if not self.excerpt:
                missing.append("excerpt")
            if not self.category_id:
                missing.append("category")
            has_sources = self.sources.exists() if self.pk else False
            if not has_sources:
                missing.append("sources")
            if missing:
                raise ValidationError({"state": f"No se puede publicar sin: {', '.join(missing)}."})

    def __str__(self):
        return self.title


class ArticleSource(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    source = models.ForeignKey("sources.Source", on_delete=models.PROTECT)
    added_by_agent = models.BooleanField(default=False)
    note = models.TextField(blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["article", "source"], name="unique_article_source")]
