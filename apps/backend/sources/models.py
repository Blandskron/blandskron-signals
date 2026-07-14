from django.db import models


class Source(models.Model):
    TYPES = [(value, value.title()) for value in ("official", "documentation", "research", "news", "analysis", "community", "social")]
    title = models.CharField(max_length=300)
    url = models.URLField()
    publisher = models.CharField(max_length=200)
    author = models.CharField(max_length=200, blank=True)
    published_at = models.DateField(null=True, blank=True)
    consulted_at = models.DateField(auto_now_add=True)
    source_type = models.CharField(max_length=32, choices=TYPES)
    confidence_note = models.TextField(blank=True)
    usage_note = models.TextField(blank=True)

    class Meta:
        ordering = ["-consulted_at", "title"]

    def __str__(self):
        return self.title
