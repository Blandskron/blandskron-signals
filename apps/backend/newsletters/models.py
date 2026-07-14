from django.conf import settings
from django.db import models


class Campaign(models.Model):
    TYPES = [(value, value.replace("_", " ").title()) for value in ("immediate", "weekly_signals", "monthly_intelligence")]
    site = models.ForeignKey("sites.Site", on_delete=models.CASCADE, related_name="newsletter_campaigns")
    name = models.CharField(max_length=180)
    campaign_type = models.CharField(max_length=32, choices=TYPES, default="weekly_signals")
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Edition(models.Model):
    STATES = [(value, value.title()) for value in ("draft", "scheduled", "sending", "sent", "cancelled")]
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="editions")
    subject = models.CharField(max_length=200)
    preview_text = models.CharField(max_length=300, blank=True)
    content_markdown = models.TextField()
    state = models.CharField(max_length=20, choices=STATES, default="draft")
    scheduled_at = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


class Delivery(models.Model):
    STATES = [(value, value.title()) for value in ("queued", "sent", "failed")]
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE, related_name="deliveries")
    subscriber = models.ForeignKey("subscribers.Subscriber", on_delete=models.CASCADE, related_name="deliveries")
    state = models.CharField(max_length=12, choices=STATES, default="queued")
    provider_message_id = models.CharField(max_length=200, blank=True)
    error_message = models.TextField(blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["edition", "subscriber"], name="unique_delivery_per_edition")]
