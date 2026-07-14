from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone
from subscribers.models import Subscriber

from newsletters.models import Delivery, Edition


class Command(BaseCommand):
    help = "Envía ediciones programadas a suscriptores activos."

    def handle(self, *args, **options):
        editions = Edition.objects.filter(state="scheduled", scheduled_at__lte=timezone.now()).select_related("campaign")
        total = 0
        for edition in editions:
            edition.state = "sending"
            edition.save(update_fields=["state"])
            subscribers = Subscriber.objects.filter(site=edition.campaign.site, state="active")
            for subscriber in subscribers:
                delivery, created = Delivery.objects.get_or_create(edition=edition, subscriber=subscriber)
                if not created and delivery.state == "sent":
                    continue
                try:
                    send_mail(edition.subject, edition.content_markdown, settings.DEFAULT_FROM_EMAIL, [subscriber.email], fail_silently=False)
                except Exception as exc:  # noqa: BLE001
                    delivery.state = "failed"
                    delivery.error_message = str(exc)[:2000]
                    delivery.save(update_fields=["state", "error_message"])
                    continue
                delivery.state = "sent"
                delivery.sent_at = timezone.now()
                delivery.save(update_fields=["state", "sent_at"])
                total += 1
            edition.state = "sent"
            edition.sent_at = timezone.now()
            edition.save(update_fields=["state", "sent_at"])
        self.stdout.write(self.style.SUCCESS(f"Envíos completados: {total}"))
