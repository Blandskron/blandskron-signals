from django.test import TestCase
from sites.models import Site

from .models import Subscriber


class SubscriberTests(TestCase):
    def setUp(self):
        self.site = Site.objects.create(name="Signals", domain="localhost", slug="signals")

    def test_double_opt_in_confirmation(self):
        subscriber = Subscriber.objects.create(site=self.site, email="reader@example.com")
        token = subscriber.issue_confirmation_token()
        self.assertTrue(subscriber.confirm(token))
        self.assertEqual(subscriber.state, "active")

    def test_invalid_token_does_not_confirm(self):
        subscriber = Subscriber.objects.create(site=self.site, email="reader@example.com")
        subscriber.issue_confirmation_token()
        self.assertFalse(subscriber.confirm("invalid"))
        self.assertEqual(subscriber.state, "pending")

    def test_unsubscribe_changes_state(self):
        subscriber = Subscriber.objects.create(site=self.site, email="reader@example.com", state="active")
        subscriber.unsubscribe()
        self.assertEqual(subscriber.state, "unsubscribed")
