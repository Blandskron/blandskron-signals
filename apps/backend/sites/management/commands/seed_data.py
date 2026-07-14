from articles.models import Category
from django.core.management.base import BaseCommand
from editorial.models import EditorialGuideline
from newsletters.models import Campaign
from trends.models import Trend

from sites.models import Site


class Command(BaseCommand):
    help = "Crea datos editoriales mínimos para desarrollo local."

    def handle(self, *args, **options):
        site, site_created = Site.objects.get_or_create(slug="blandskron-signals", defaults={"name": "Blandskron Signals", "domain": "localhost", "editorial_language": "es", "timezone": "America/Santiago"})
        EditorialGuideline.objects.get_or_create(site=site, defaults={"tone": "Claro, profesional y accesible.", "audience": "Personas técnicas y líderes de negocio.", "allowed_topics": ["IA", "software", "agentes", "automatización", "ciberseguridad"], "restricted_topics": ["spam", "afirmaciones sin fuentes"], "seo_requirements": ["título", "resumen", "metadescripción", "fuentes"], "agent_instructions": "Consultar fuentes primarias y enviar borradores a revisión."})
        categories = [("Inteligencia artificial", "inteligencia-artificial"), ("Desarrollo", "desarrollo"), ("Automatización", "automatizacion"), ("Ciberseguridad", "ciberseguridad"), ("Negocios y tecnología", "negocios-tecnologia")]
        for name, slug in categories:
            Category.objects.get_or_create(site=site, slug=slug, defaults={"name": name})
        trends = [("Agentes operativos", "agentes-operativos", "artificial_intelligence", "Sistemas que pueden ejecutar flujos de trabajo con supervisión humana."), ("Automatización verificable", "automatizacion-verificable", "automation", "Automatización con trazabilidad, permisos y auditoría."), ("Seguridad de la cadena de software", "seguridad-cadena-software", "cybersecurity", "Controles para dependencias, código y procesos de entrega.")]
        for name, slug, category, description in trends:
            Trend.objects.get_or_create(slug=slug, defaults={"name": name, "category": category, "description": description, "state": "emerging", "impact_level": 7, "maturity_level": 4})
        Campaign.objects.get_or_create(site=site, campaign_type="weekly_signals", defaults={"name": "Weekly Signals", "description": "Resumen semanal de señales tecnológicas."})
        self.stdout.write(self.style.SUCCESS(f"Datos iniciales listos. Sitio {'creado' if site_created else 'existente'}: {site.slug}"))
