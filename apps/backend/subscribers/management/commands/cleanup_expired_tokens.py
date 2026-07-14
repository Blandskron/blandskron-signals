from django.core.management.base import BaseCommand
from django.utils import timezone

from subscribers.models import Subscriber


class Command(BaseCommand):
    help = "Limpia tokens de confirmación expirados."

    def handle(self, *args, **options):
        count = Subscriber.objects.filter(token_expires_at__lt=timezone.now()).update(confirmation_token_hash="", token_expires_at=None)
        self.stdout.write(self.style.SUCCESS(f"Tokens limpiados: {count}"))
