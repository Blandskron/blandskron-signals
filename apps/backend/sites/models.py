from django.db import models


class Site(models.Model):
    name = models.CharField(max_length=120)
    domain = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)
    editorial_language = models.CharField(max_length=10, default="es")
    timezone = models.CharField(max_length=64, default="America/Santiago")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
