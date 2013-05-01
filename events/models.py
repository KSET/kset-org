# -*- coding: utf-8 -*-

from datetime import datetime

from django.db import models

from filebrowser.fields import FileBrowseField
from tinymce.models import HTMLField
from tagging_autocomplete.models import TagAutocompleteField


class EventManager(models.Manager):

    def get_today(self):
        return self.filter(date=datetime.now())

    def get_forward(self):
        return self.filter(date__gt=datetime.now()).order_by('date')

    def is_reserved(self, date):
        if self.filter(date=date):
            return True
        else:
            return False


class Event(models.Model):
    title = models.CharField(u'Naslov', max_length=192)
    date = models.DateField(u'Datum')
    time = models.TimeField(u'Vrijeme', null=True, blank=True)
    description = HTMLField(u'Opis', blank=True)
    content = HTMLField(u'Sadržaj', blank=True)
    tags = TagAutocompleteField(blank=True)
    slug = models.SlugField(blank=True, max_length=128)
    announce = models.BooleanField(u'Najavi')
    daytime = models.BooleanField(u'Dnevni')
    price = models.CharField(u'Cijena', max_length=16, null=True, blank=True)
    thumb = FileBrowseField(u'Sličica', max_length=255, null=True, blank=True)
    objects = EventManager()

    class Meta:
        verbose_name = 'događaj'
        verbose_name_plural = 'događaji'

    # rss feed uses this
    def get_absolute_url(self):
        return '/dogadaj/%s/' % self.slug

    def __unicode__(self):
        return u'%s %s' % (self.title, self.date)

    @staticmethod
    def get_frontpage_events():
        return Event.objects.filter(date__gte=datetime.now()).filter(
            daytime=False, announce=True).order_by('date')[:3]

    @staticmethod
    def get_frontpage_daytime_events():
        return Event.objects.filter(date__gte=datetime.now()).filter(
            announce=True, daytime=True).order_by('date')[:3]
