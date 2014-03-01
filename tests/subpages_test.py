from django.test import TestCase

from .base import BaseTestClient
from subpages.views import DIVISIONS, PROJECTS


__all__ = ['SubpageViewTest']


class SubpageViewTest(TestCase):

    def setUp(self):
        super(SubpageViewTest, self).setUp()
        self.client = BaseTestClient()

    def test_subpage_division(self):
        for d in DIVISIONS:
            response = self.client.get('subpage_division', division=d['id'])
            self.assertEquals(200, response.status_code)

    def test_subpage_projects(self):
        for p in PROJECTS:
            response = self.client.get('subpage_project', project=p['id'])
            self.assertEquals(200, response.status_code)

    def test_subpage_alumni(self):
        response = self.client.get('subpage_alumni')
        self.assertEquals(200, response.status_code)

    def test_multimedia(self):
        response = self.client.get('subpage_multimedia')
        self.assertEquals(200, response.status_code)
