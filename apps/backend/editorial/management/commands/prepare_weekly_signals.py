from django.core.management.base import BaseCommand
from newsletters.models import Campaign, Edition
from sites.models import Site

from editorial.automation import tracked_run
from editorial.models import EditorialTask


class Command(BaseCommand):
    help = "Prepara tareas y un borrador de Weekly Signals."

    def handle(self, *args, **options):
        with tracked_run("weekly_signals") as run:
            site = Site.objects.filter(is_active=True).first()
            if not site:
                self.stderr.write("No existe un sitio activo.")
                return
            task, created = EditorialTask.objects.get_or_create(site=site, task_type="newsletter", state="pending", title="Preparar Weekly Signals", defaults={"instructions": "Seleccionar la señal principal, tendencias y recomendación técnica de la semana."})
            campaign, _ = Campaign.objects.get_or_create(site=site, campaign_type="weekly_signals", defaults={"name": "Weekly Signals"})
            edition = Edition.objects.create(campaign=campaign, subject="Weekly Signals — borrador", content_markdown="## Weekly Signals\n\nCompletar con la revisión editorial de la semana.")
            run.items_created = int(created) + 1
            run.metadata = {"task_id": task.pk, "edition_id": edition.pk}
            self.stdout.write(self.style.SUCCESS(f"Newsletter borrador: {edition.pk}"))
