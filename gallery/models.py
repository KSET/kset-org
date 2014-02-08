# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models

from filebrowser.fields import FileBrowseField
from tinymce.models import HTMLField

from .helpers import parse_filename, exclude_fb_versions


class Photographer(models.Model):
    name = models.CharField('Ime i prezime', max_length=32)
    url = models.URLField('Web stranica', max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Fotograf"
        verbose_name_plural = "Fotografi"
        ordering = ('name',)


class Album(models.Model):

    LIVE = 'live'
    FOTO = 'foto'
    SCLIVE = 'sclive'

    CATEGORIES = (
        (LIVE, 'LIVE'),
        (FOTO, 'FOTO'),
        (SCLIVE, 'SCLIVE'),
    )

    upload_path = FileBrowseField("Putanja do albuma", max_length=255,
        directory="gallery/", null=True, blank=True)
    title = models.CharField('Ime albuma', max_length=255, unique=False)
    slug = models.SlugField()
    description = HTMLField('Kratak opis', max_length=255)
    date_of_event = models.DateField('Datum događaja')
    date_of_upload = models.DateTimeField(auto_now=True)
    photographer = models.ForeignKey(Photographer, null=True)
    initial = models.BooleanField(default=True)
    thumb = FileBrowseField("Sličica", max_length=255, directory="gallery/",
        null=False, blank=False)
    category = models.CharField("Kategorija", null=False, max_length=25,
        choices=CATEGORIES)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = "Album"
        verbose_name_plural = "Albumi"
        permissions = (
            ('view_album', 'View Album'),)

    def save(self):
        super(Album, self).save()
        if (self.initial):
            if (not self.upload_path.is_empty):
                self.initial = False
                super(Album, self).save()
                full_path_to_album = settings.MEDIA_ROOT+self.upload_path.path

                for filename in exclude_fb_versions(full_path_to_album):
                    parsed = parse_filename(filename)
                    if (parsed):
                        new_image = Image.objects.create(title=parsed['name'],
                            slug=parsed['slug'],
                            upload_path=str(self.upload_path.path) + '/' + parsed['name_full'],
                            date_of_event=parsed['date'],
                            photographer=self.photographer)
                        new_image.album.add(self)


class Image(models.Model):
    title = models.CharField(u'Naziv slike', max_length=255, unique=False)
    slug = models.SlugField()
    caption = HTMLField(u'Kratak opis', null=True, blank=True, max_length=255)
    photographer = models.ForeignKey(Photographer, null=True)
    date_of_event = models.DateField(u'Datum događaja')
    date_of_upload = models.DateTimeField(auto_now=True)
    album = models.ManyToManyField(Album, related_name='images')
    upload_path = FileBrowseField(u'Putanja do slike', max_length=255,
        format="Image", directory='gallery/', null=False, blank=False)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = "Slika"
        verbose_name_plural = "Slike"
