from datetime import datetime, timedelta

from django.test import TestCase

from .base import BaseTestClient
from .factories import EventFactory
from newsletter.models import Subscription


__all__ = ['EventsViewTest']


class EventsViewTest(TestCase):

    def setUp(self):
        super(EventsViewTest, self).setUp()
        self.client = BaseTestClient()

    def test_get_events_archive(self):
        response = self.client.get('events_archive')
        self.assertEquals(200, response.status_code)

    def test_get_archive_by_year(self):
        year = datetime.now().year
        response = self.client.get('events_archive_year', year=year)
        self.assertEquals(200, response.status_code)

    def test_get_newsletter(self):
        response = self.client.get('newsletter')
        self.assertEquals(200, response.status_code)

    def test_get_newsletter_range(self):
        date_from = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        date_til = datetime.now().strftime('%Y-%m-%d')
        response = self.client.get('newsletter', {'from': date_from, 'till': date_til})
        self.assertEquals(200, response.status_code)

    def test_get_event_by_slug(self):
        event = EventFactory()
        response = self.client.get('event_slug', slug=event.slug)
        self.assertEquals(200, response.status_code)

    def test_get_events_by_data(self):
        EventFactory(date=datetime.now())
        date_str = datetime.now().strftime('%Y-%m-%d')
        response = self.client.get('events_date', date=date_str)
        self.assertEquals(200, response.status_code)

    def test_event_calendar(self):
        response = self.client.get('calendar')
        self.assertEquals(200, response.status_code)

    def test_subscribe_to_newsletter_with_get_fail(self):
        response = self.client.get('subscribe', {'email': 'invalidEmail'})
        self.assertEquals(405, response.status_code)

    def test_subscribe_to_newsletter_with_invalid_email_fail(self):
        response = self.client.post('subscribe', {'email': 'invalid_email_text'})
        self.assertEquals(400, response.status_code)

    def test_subscribe_to_newsletter(self):
        response = self.client.post('subscribe', {'email': 'm@email.com'})
        self.assertEquals(200, response.status_code)

        self.assertEquals(1, Subscription.objects.count())
