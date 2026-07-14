from articles.models import Category
from django.core.management import call_command
from django.test import TestCase
from editorial.models import EditorialGuideline
from newsletters.models import Campaign
from trends.models import Trend

from sites.models import Site


class SeedDataTests(TestCase):
    def test_seed_data_is_idempotent(self):
        call_command("seed_data")
        call_command("seed_data")
        self.assertEqual(Site.objects.count(), 1)
        self.assertEqual(Category.objects.count(), 5)
        self.assertEqual(Trend.objects.count(), 3)
        self.assertEqual(EditorialGuideline.objects.count(), 1)
        self.assertEqual(Campaign.objects.count(), 1)
