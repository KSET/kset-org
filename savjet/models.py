from django.db import models

from django.contrib.auth.models import User
from datetime import datetime

class Zapisnik(models.Model):
      author = models.ForeignKey(User)
      date = models.DateTimeField()
      title = models.CharField(max_length=100)
      content = models.TextField( "sadrzaj", null=True, blank=True )

      class Meta:
          verbose_name = "Zapisnik"
          verbose_name_plural = "Zapisnici"


