from audit.models import AutomationRun
from django.core.management import call_command
from django.test import TestCase
from sites.models import Site

from .models import EditorialTask


class EditorialAutomationTests(TestCase):
    def test_daily_research_is_idempotent_and_audited(self):
        Site.objects.create(name="Signals", domain="localhost", slug="signals")
        call_command("run_daily_research")
        call_command("run_daily_research")
        self.assertEqual(EditorialTask.objects.filter(task_type="research").count(), 1)
        self.assertEqual(AutomationRun.objects.filter(job_name="daily_research", state="completed").count(), 2)
