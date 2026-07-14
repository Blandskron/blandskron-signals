from django.contrib import admin

from .models import Campaign, Delivery, Edition


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ("name", "campaign_type", "site", "is_active", "created_at")
    list_filter = ("campaign_type", "is_active")


@admin.register(Edition)
class EditionAdmin(admin.ModelAdmin):
    list_display = ("subject", "campaign", "state", "scheduled_at", "sent_at")
    list_filter = ("state", "campaign__campaign_type")


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ("edition", "subscriber", "state", "sent_at")
    list_filter = ("state",)
    readonly_fields = [field.name for field in Delivery._meta.fields]
