from django.core.management.base import BaseCommand
from sites.models import Site

from newsletters.models import Campaign, Edition


class Command(BaseCommand):
    help = "Crea un borrador de Weekly Signals para revisión editorial."

    def handle(self, *args, **options):
        site = Site.objects.filter(is_active=True).first()
        if not site:
            self.stderr.write("No existe un sitio activo.")
            return
        campaign, _ = Campaign.objects.get_or_create(site=site, campaign_type="weekly_signals", defaults={"name": "Weekly Signals"})
        edition = Edition.objects.create(campaign=campaign, subject="Weekly Signals — borrador", preview_text="Resumen semanal de Blandskron Signals", content_markdown="## Weekly Signals\n\nCompletar después de la revisión editorial.")
        self.stdout.write(self.style.SUCCESS(f"Borrador creado: {edition.pk}"))
