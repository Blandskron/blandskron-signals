from django.contrib import admin

from .models import AuditEvent, AutomationRun


@admin.register(AuditEvent)
class AuditEventAdmin(admin.ModelAdmin):
    list_display = ("action", "entity_type", "entity_id", "actor", "created_at")
    list_filter = ("action", "entity_type")
    readonly_fields = [field.name for field in AuditEvent._meta.fields]


@admin.register(AutomationRun)
class AutomationRunAdmin(admin.ModelAdmin):
    list_display = ("job_name", "state", "items_created", "started_at", "finished_at")
    list_filter = ("job_name", "state")
    readonly_fields = [field.name for field in AutomationRun._meta.fields]
