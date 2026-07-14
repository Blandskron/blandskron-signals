from django.contrib import admin

from .models import Trend


@admin.register(Trend)
class TrendAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "state", "impact_level", "maturity_level")
    list_filter = ("category", "state")
    prepopulated_fields = {"slug": ("name",)}
