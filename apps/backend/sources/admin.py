from django.contrib import admin

from .models import Source


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ("title", "publisher", "source_type", "published_at", "consulted_at")
    list_filter = ("source_type",)
    search_fields = ("title", "publisher", "url")
