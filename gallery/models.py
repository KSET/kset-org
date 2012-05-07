#coding: utf8

import re

from django.db import models
from filebrowser.fields import FileBrowseField
from filebrowser import base
from filebrowser.settings import *
import settings.base as settings

from functions import *
from datetime import datetime
import string

from tinymce.models import HTMLField


# Create your models here.

class Image(models.Model):
  title = models.CharField('Naziv slike', max_length=255, unique=False)
  slug = models.SlugField()
  caption = models.CharField('Kratak opis', null=True, blank=True, max_length=255)
  photographer = models.ForeignKey("Photographer", null=True)
  date_of_event = models.DateField('Datum događaja')
  date_of_upload = models.DateTimeField(auto_now = True)
  album = models.ManyToManyField('Album')
  upload_path = FileBrowseField( "Putanja do slike", max_length=255, format="Image", directory="gallery/", null=False, blank=False  )
  
  def __unicode__(self):
    return self.title

  class Meta:
    verbose_name = "Slika"
    verbose_name_plural = "Slike"

class Album(models.Model):
  upload_path = FileBrowseField( "Putanja do albuma", max_length=255, directory="gallery/", null=True, blank=True  )
  title = models.CharField('Ime albuma', max_length=255, unique=False)
  slug = models.SlugField()
  description = HTMLField('Kratak opis', max_length=255)
  date_of_event = models.DateField('Datum događaja')
  date_of_upload = models.DateTimeField(auto_now=True)
  photographer = models.ForeignKey("Photographer", null=True)
  initial = models.BooleanField(default=True)
  thumb = FileBrowseField( "Sličica", max_length=255, directory="gallery/", null=False, blank=False  )
  category = models.CharField("Kategorija", null=False, max_length = 25, choices = (('LIVE', 'LIVE'),('FOTO','FOTO'), ('SCLIVE','SCLIVE')))
  

  def save(self):
    super(Album, self).save()
    if (self.initial):
      
      if (self.upload_path.is_empty != True ):
          self.initial = False
          super(Album, self).save()

          filter_re = []
          for exp in EXCLUDE:
              filter_re.append(re.compile(exp))
          for k,v in VERSIONS.iteritems():
            exp = (r'_%s.(%s)') % (k, '|'.join(EXTENSION_LIST))
            filter_re.append(re.compile(exp))
          filtered_images = []
          images = []
          for image in os.listdir(settings.MEDIA_ROOT+self.upload_path.path):
            # EXCLUDE FILES MATCHING VERSIONS_PREFIX OR ANY OF THE EXCLUDE PATTERNS
            for re_prefix in filter_re:
              if re_prefix.search(image):
                filtered_images.append(image)
            if image not in filtered_images:
              images.append(image)
          ##new images in album
          for filename in images:
            parsed = parse_filename(filename)
            if (parsed):
              new_image = Image(title = parsed['name'], slug = parsed['slug'], upload_path = str(self.upload_path.path) + '/' + parsed['name_full'], date_of_event = parsed['date'], photographer = Photographer.objects.get(id = self.photographer.id))
              new_image.save()
              new_image.album.add(self)


  def __unicode__(self):
    return self.title

  class Meta:
    verbose_name = "Album"
    verbose_name_plural = "Albumi"
    permissions = (
            ('view_album', 'View Album'),
        )

class Photographer(models.Model):
  name = models.CharField('Ime i prezime', max_length=32)

  def __unicode__(self):
    return self.name

  class Meta:
    verbose_name = "Fotograf"
    verbose_name_plural = "Fotografi"
    ordering = ('name',)

