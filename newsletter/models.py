from django.db import models


class Subscription(models.Model):
    email = models.EmailField(unique=True)

    class Meta:
        verbose_name = 'pretplata'
        verbose_name_plural = 'pretplate'

        def __unicode__(self):
            return u'%s' % self.email
