#coding: utf8

from django.db import models
from filebrowser.fields import FileBrowseField
from tagging.fields import TagField
from tagging_autocomplete.models import TagAutocompleteField
from tinymce.models import HTMLField

from datetime import datetime

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
    title = models.CharField('naslov', max_length=192)
    date = models.DateField( 'datum' )
    time = models.TimeField( 'vrijeme', null=True, blank=True )
    description = HTMLField( 'opis', blank=True )
    content = HTMLField( 'sadržaj', blank=True )
    tags = TagAutocompleteField( blank=True )
    slug = models.SlugField( blank=True, max_length=128 )
    announce = models.BooleanField( 'najavi' )
    daytime = models.BooleanField('Dnevni')
    price = models.CharField('cijena', max_length=16, null=True, blank=True )
    thumb = FileBrowseField( 'sličica', max_length=255, null=True, blank=True )
    objects = EventManager()

    class Meta:
        verbose_name = 'događaj'
        verbose_name_plural = 'događaji'

    # rss feed uses this
    def get_absolute_url(self):
        return '/dogadaj/%s/' % self.slug

    def __unicode__(self):
        return u'%s %s' % (self.title, self.date)

