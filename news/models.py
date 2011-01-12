#coding: utf8

from django.db import models
from filebrowser.fields import FileBrowseField

class News(models.Model):
    subject = models.CharField( 'naslov', max_length=192 )
    description = models.TextField( 'opis', blank=True )
    content = models.TextField( 'sadržaj',blank=True )
    publish = models.DateTimeField( 'datum objave')
    expire = models.DateTimeField( 'datum isteka', null=True, blank=True )
    thumb = FileBrowseField( 'sličica', max_length=255, blank=True  ) 
    slug = models.SlugField( blank=True, max_length=128 )
 
    class Meta:
        verbose_name = 'vijest'
        verbose_name_plural = 'vijesti'

    def __unicode__(self):
        return self.subject

