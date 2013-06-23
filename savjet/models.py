from django.db import models
from django.contrib.auth.models import User

from tinymce.models import HTMLField


class Zapisnik(models.Model):
    author = models.ForeignKey(User)
    date = models.DateTimeField()
    title = models.CharField(max_length=100)
    content = HTMLField("Sadrzaj", null=True, blank=True)

    class Meta:
        verbose_name = "Zapisnik"
        verbose_name_plural = "Zapisnici"


class Dezurstva(models.Model):
    start = models.DateField()
    end = models.DateField()
    content = HTMLField("Dezurne sekcije")

    class Meta:
        verbose_name = "Dezurstvo"
        verbose_name_plural = "Dezurstva"
