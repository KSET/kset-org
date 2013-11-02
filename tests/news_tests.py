from django.test import TestCase

from .base import BaseTestClient

from .factories import NewsFactory
from news.models import News

__all__ = ['NewsViewTest']


class NewsViewTest(TestCase):

    def setUp(self):
        super(NewsViewTest, self).setUp()
        self.client = BaseTestClient()

    def test_get_news_by_slug(self):
        news = NewsFactory()
        response = self.client.get('news_slug', slug=news.slug)
        self.assertEquals(200, response.status_code)

    def test_get_homepage(self):
        news = NewsFactory()
        response = self.client.get('index')
        self.assertEquals(200, response.status_code)

    def test_get_news_archive(self):
        news = NewsFactory()
        response = self.client.get('news_archive')
        self.assertEquals(200, response.status_code)
