from django.test import TestCase

from .base import BaseTestClient
from .factories import SubpageFactory


__all__ = ['SubpageViewTest']


class SubpageViewTest(TestCase):

    def setUp(self):
        super(SubpageViewTest, self).setUp()
        self.client = BaseTestClient()

    def test_subpage_by_slug(self):
        subpage = SubpageFactory()
        response = self.client.get('subpage_slug', slug=subpage.slug)
        self.assertEquals(200, response.status_code)

    def test_multimedia(self):
        response = self.client.get('multimedia')
        self.assertEquals(200, response.status_code)
