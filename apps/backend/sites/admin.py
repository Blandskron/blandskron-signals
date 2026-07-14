from django.contrib import admin

from .models import Site


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ("name", "domain", "is_active", "editorial_language")
    prepopulated_fields = {"slug": ("name",)}
