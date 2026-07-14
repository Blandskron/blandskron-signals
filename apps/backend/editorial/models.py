from django.conf import settings
from django.db import models


class EditorialGuideline(models.Model):
    site = models.OneToOneField("sites.Site", on_delete=models.CASCADE, related_name="guidelines")
    tone = models.TextField(default="Claro, profesional y accesible.")
    audience = models.TextField(blank=True)
    allowed_topics = models.JSONField(default=list, blank=True)
    restricted_topics = models.JSONField(default=list, blank=True)
    seo_requirements = models.JSONField(default=list, blank=True)
    agent_instructions = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Guía editorial: {self.site}"


class EditorialTask(models.Model):
    TYPES = [(value, value.replace("_", " ").title()) for value in ("research", "draft", "review", "update_article", "newsletter", "source_check")]
    STATES = [(value, value.replace("_", " ").title()) for value in ("pending", "in_progress", "blocked", "completed", "cancelled")]
    site = models.ForeignKey("sites.Site", on_delete=models.CASCADE, related_name="editorial_tasks")
    task_type = models.CharField(max_length=24, choices=TYPES)
    title = models.CharField(max_length=200)
    instructions = models.TextField(blank=True)
    state = models.CharField(max_length=20, choices=STATES, default="pending")
    article = models.ForeignKey("articles.Article", null=True, blank=True, on_delete=models.SET_NULL, related_name="editorial_tasks")
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="assigned_editorial_tasks")
    due_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["state", "due_at", "-created_at"]

    def __str__(self):
        return self.title
