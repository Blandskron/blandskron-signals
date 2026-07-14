from datetime import date

from django.core.management.base import BaseCommand
from sites.models import Site

from editorial.automation import tracked_run
from editorial.models import EditorialTask


class Command(BaseCommand):
    help = "Crea la tarea diaria de investigación editorial."

    def handle(self, *args, **options):
        with tracked_run("daily_research") as run:
            site = Site.objects.filter(is_active=True).first()
            if not site:
                self.stderr.write("No existe un sitio activo.")
                return
            title = f"Investigación diaria — {date.today().isoformat()}"
            task, created = EditorialTask.objects.get_or_create(site=site, title=title, defaults={"task_type": "research", "instructions": "Consultar fuentes primarias, revisar duplicados y registrar señales relevantes."})
            run.items_created = int(created)
            run.metadata = {"task_id": task.pk}
            self.stdout.write(self.style.SUCCESS(f"Tarea diaria: {task.pk}"))
