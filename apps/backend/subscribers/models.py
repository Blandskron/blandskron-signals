import hashlib
import secrets
from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Subscriber(models.Model):
    STATES = [(value, value.title()) for value in ("pending", "active", "unsubscribed", "blocked", "bounced")]
    email = models.EmailField()
    site = models.ForeignKey("sites.Site", on_delete=models.CASCADE, related_name="subscribers")
    state = models.CharField(max_length=20, choices=STATES, default="pending")
    all_articles = models.BooleanField(default=True)
    weekly_digest = models.BooleanField(default=True)
    artificial_intelligence = models.BooleanField(default=True)
    development = models.BooleanField(default=True)
    automation = models.BooleanField(default=True)
    business_technology = models.BooleanField(default=True)
    featured_analysis_only = models.BooleanField(default=False)
    confirmation_token_hash = models.CharField(max_length=64, blank=True)
    token_expires_at = models.DateTimeField(null=True, blank=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["site", "email"], name="unique_subscriber_per_site")]
        ordering = ["-created_at"]

    def issue_confirmation_token(self):
        raw_token = secrets.token_urlsafe(32)
        self.confirmation_token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
        self.token_expires_at = timezone.now() + timedelta(days=2)
        self.save(update_fields=["confirmation_token_hash", "token_expires_at", "updated_at"])
        return raw_token

    def send_confirmation(self, raw_token):
        url = f"{getattr(settings, 'SITE_URL', 'http://localhost:8000')}{reverse('subscriber-confirm', kwargs={'token': raw_token})}"
        send_mail("Confirma tu suscripción a Blandskron Signals", f"Confirma tu suscripción aquí: {url}", settings.DEFAULT_FROM_EMAIL, [self.email], fail_silently=False)

    def confirm(self, raw_token):
        valid_hash = hashlib.sha256(raw_token.encode()).hexdigest() == self.confirmation_token_hash
        if not valid_hash or not self.token_expires_at or self.token_expires_at < timezone.now():
            return False
        self.state = "active"
        self.confirmed_at = timezone.now()
        self.confirmation_token_hash = ""
        self.token_expires_at = None
        self.save(update_fields=["state", "confirmed_at", "confirmation_token_hash", "token_expires_at", "updated_at"])
        return True

    def unsubscribe(self):
        self.state = "unsubscribed"
        self.unsubscribed_at = timezone.now()
        self.save(update_fields=["state", "unsubscribed_at", "updated_at"])

    def __str__(self):
        return self.email
