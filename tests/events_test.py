from django.test import TestCase

from .base import BaseTestClient


__all__ = ['EventsViewTest']


class EventsViewTest(TestCase):

    def setUp(self):
        super(EventsViewTest, self).setUp()
        self.client = BaseTestClient()

    def test_get_events_archive(self):
        # self.client.login(username='super_user',
        #     password='foobar')

        response = self.client.get('events-archive')
        self.assertEquals(200, response.status_code)

    def test_get_newsletter(self):
        response = self.client.get('newsletter')
        self.assertEquals(200, response.status_code)
