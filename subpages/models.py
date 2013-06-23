#coding: utf8

from django.db import models

from filebrowser.fields import FileBrowseField
from tinymce.models import HTMLField


class Category(models.Model):
    name = models.CharField('naziv', max_length=128)
    slug = models.SlugField()
    parent = models.ForeignKey('self', null=True, blank=True, verbose_name='nad-kategorije')

    class Meta:
        verbose_name = 'kategorija'
        verbose_name_plural = 'kategorije'

    def __unicode__(self):
        return self.name


class Subpage(models.Model):
    title = models.CharField('naslov', max_length=128)
    slug = models.SlugField()
    last_edit = models.DateTimeField('zadnja promjena', auto_now=True)
    description = HTMLField('opis', blank=True)
    content = HTMLField('sadržaj', blank=True)
    thumb = FileBrowseField('sličica', max_length=255, null=True, blank=True)
    category = models.ForeignKey(Category, null=True, blank=True, verbose_name='kategorija')

    class Meta:
        verbose_name = 'podstranica'
        verbose_name_plural = 'podstranice'

    def __unicode__(self):
        return self.title
