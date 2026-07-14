from django.contrib import admin

from .models import Subscriber


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "site", "state", "weekly_digest", "confirmed_at", "created_at")
    list_filter = ("state", "weekly_digest", "site")
    search_fields = ("email",)
    readonly_fields = ("confirmation_token_hash", "token_expires_at", "confirmed_at", "unsubscribed_at", "created_at", "updated_at")
