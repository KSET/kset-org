# -*- coding: utf-8 -*-

from datetime import datetime

from django.db import models

from filebrowser.fields import FileBrowseField
from tinymce.models import HTMLField


class News(models.Model):
    subject = models.CharField(u'Naslov', max_length=192)
    description = HTMLField(u'Opis', blank=True)
    content = HTMLField(u'Sadržaj', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expire_at = models.DateTimeField(null=True)
    sticky = models.BooleanField(u'Sticky', default=False)
    thumb = FileBrowseField(u'Sličica', max_length=255, blank=True)
    slug = models.SlugField(blank=True, max_length=128, unique=True)

    class Meta:
        verbose_name = 'vijest'
        verbose_name_plural = 'vijesti'

    def __unicode__(self):
        return self.subject

    @staticmethod
    def get_frontpage_news():
        return News.objects.filter(expire_at__gte=datetime.today()).exclude(sticky=True)[:3]

    @staticmethod
    def get_sticky_news():
        return News.objects.filter(sticky=True).order_by('-created_at')
