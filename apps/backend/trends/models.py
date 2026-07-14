from django.db import models


class Trend(models.Model):
    CATEGORIES = [(value, value.replace("_", " ").title()) for value in ("artificial_intelligence", "development", "automation", "infrastructure", "cybersecurity", "business", "open_source", "user_experience")]
    STATES = [(value, value.title()) for value in ("detected", "emerging", "growing", "mainstream", "declining", "watching")]
    name = models.CharField(max_length=160)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=32, choices=CATEGORIES)
    description = models.TextField()
    state = models.CharField(max_length=20, choices=STATES, default="detected")
    impact_level = models.PositiveSmallIntegerField(default=0)
    maturity_level = models.PositiveSmallIntegerField(default=0)
    detected_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
