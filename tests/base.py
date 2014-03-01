import json

from django.test.client import Client, MULTIPART_CONTENT
from django.core.urlresolvers import reverse

__all__ = ['BaseTestClient']


class BaseTestClient(Client):

    @staticmethod
    def process(response):
        try:
            response.json = json.loads(response.content)
        except:
            response.json = None
        finally:
            return response

    @staticmethod
    def _kwargs2extra(extra, kwargs, args):
        for arg in args:
            if arg in kwargs:
                extra[arg] = kwargs.pop(arg)

    def get(self, url_name, data={}, follow=False, extra={}, *args, **kwargs):
        self._kwargs2extra(extra, kwargs, ['wsgi.url_scheme', 'SERVER_NAME',
            'SERVER_PORT'])
        if not url_name.startswith('/'):
            url_name = reverse(url_name, args=args, kwargs=kwargs)

        return self.process(
            super(BaseTestClient, self).get(
                url_name,
                data=data,
                follow=follow,
                **extra))

    def post(self, url_name, data={}, content_type=MULTIPART_CONTENT,
            follow=False, extra={}, *args, **kwargs):
        return self.process(
            super(BaseTestClient, self).post(
                reverse(url_name, args=args, kwargs=kwargs),
                content_type=content_type,
                data=data,
                follow=follow,
                **extra))

    def put(self, url_name, data={}, content_type=MULTIPART_CONTENT,
            follow=False, *args, **kwargs):
        return self.process(
            super(BaseTestClient, self).put(
                reverse(url_name, args=args, kwargs=kwargs),
                content_type=content_type, data=data, follow=follow))

    def delete(self, url_name, data={}, content_type=MULTIPART_CONTENT,
            follow=False, *args, **kwargs):
        return self.process(
            super(BaseTestClient, self).delete(
                reverse(url_name, args=args, kwargs=kwargs),
                content_type=content_type, data=data, follow=follow))
