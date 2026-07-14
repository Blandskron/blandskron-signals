from django.contrib import admin

from .models import EditorialGuideline, EditorialTask


@admin.register(EditorialGuideline)
class EditorialGuidelineAdmin(admin.ModelAdmin):
    list_display = ("site", "updated_at")


@admin.register(EditorialTask)
class EditorialTaskAdmin(admin.ModelAdmin):
    list_display = ("title", "task_type", "state", "site", "assigned_to", "due_at")
    list_filter = ("task_type", "state", "site")
    search_fields = ("title", "instructions")
