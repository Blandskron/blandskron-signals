from datetime import timedelta

from articles.models import Article
from django.core.management.base import BaseCommand
from django.utils import timezone

from editorial.automation import tracked_run
from editorial.models import EditorialTask


class Command(BaseCommand):
    help = "Crea tareas de revisión para Living Articles desactualizados."

    def handle(self, *args, **options):
        with tracked_run("monthly_living_article_review") as run:
            threshold = timezone.now() - timedelta(days=30)
            articles = Article.objects.filter(content_type="living_article", state="published", updated_at__lt=threshold).select_related("site")
            created = 0
            for article in articles:
                _, was_created = EditorialTask.objects.get_or_create(site=article.site, article=article, task_type="update_article", state="pending", defaults={"title": f"Revisar: {article.title}", "instructions": "Verificar enlaces, versiones, cifras, predicciones y nuevas fuentes."})
                created += int(was_created)
            run.items_created = created
            run.metadata = {"threshold_days": 30}
            self.stdout.write(self.style.SUCCESS(f"Tareas de revisión creadas: {created}"))
