#coding: utf8

import hashlib

from django.db import models
from django.conf import settings

from tinymce.models import HTMLField


__all__ = ['Group', 'Member', 'Contact', 'Address', 'MemberGroupLink']


class GroupManager(models.Manager):

    def tree(self, id=None):
        groups = self.filter(parent=id).order_by('name')

        if groups:
            for grp in groups:
                grp.childs = self.tree(grp.id)

        return groups


class Group(models.Model):
    CARD = 'iskaznica'
    DIVISION = 'sekcija'
    STATUS = 'status'

    name = models.CharField("naziv", max_length=32)
    slug = models.SlugField()
    parent = models.ForeignKey('self', null=True, blank=True, verbose_name="nad-grupa")
    description = models.CharField("opis", max_length=128, null=True, blank=True)
    objects = GroupManager()

    class Meta:
        verbose_name = "grupa"
        verbose_name_plural = "grupe"

    def __unicode__(self):
        return self.name


class MemberManager(models.Manager):

    def active(self):

        return self.all()


class Member(models.Model):
    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = "član"
        verbose_name_plural = "članovi"

    card_id = models.CharField("iskaznica", max_length=32, null=True, blank=True)
    name = models.CharField("ime", max_length=32)
    surname = models.CharField("prezime", max_length=64)
    slug = models.SlugField()
    nickname = models.CharField("nadimak", max_length=32, null=True, blank=True)
    username = models.CharField("korisničko ime", unique=True, max_length=32)
    password = models.CharField("lozinka", max_length=255, null=True, blank=True)
    birth = models.DateField("datum rođenja", null=True, blank=True)
    death = models.DateField("datum smrti", null=True, blank=True)
    comment = HTMLField("komentar", null=True, blank=True)
    groups = models.ManyToManyField(Group, through='MemberGroupLink')
    image = models.ImageField(upload_to="/", null=True, blank=True, verbose_name="slika")
    objects = MemberManager()

    def __init__(self, *args, **kwargs):
        super(Member, self).__init__(*args, **kwargs)
        self._initial_password = self.password

    def __unicode__(self):
        return self.username

    def get_username(self):
        return self.username

    def set_password(self, password):
        self.password = hashlib.md5(password+settings.SECRET_KEY).hexdigest()

    def division(self):
        """Returns division name. --> Hardcoded group ID!"""

        try:
            return MemberGroupLink.objects.filter(
                member=self.id).filter(
                group__parent=1).values(
                'group__name')[0]["group__name"]
        except:
            return u'---'

    def card(self):
        """Returns card. --> Hardcoded group ID!"""

        try:
            return MemberGroupLink.objects.filter(
                member=self.id).filter(
                group__parent=2).values(
                'group__name')[0]["group__name"]
        except:
            return u'---'


class MemberGroupLink(models.Model):
    member = models.ForeignKey(Member, verbose_name="član")
    group = models.ForeignKey(Group, verbose_name="grupa")
    date_start = models.DateField("početak", null=True, blank=True)
    date_end = models.DateField("kraj", null=True, blank=True)

    class Meta:
        verbose_name = "članstvo"
        verbose_name_plural = "članstva"


class Contact(models.Model):
    TYPE_EMAIL = 'email'
    TYPE_PHONE = 'phone'
    TYPE_CELL = 'cell'

    TYPES = (
        (TYPE_EMAIL, 'E-mail'),
        (TYPE_PHONE, 'Telefon'),
        (TYPE_CELL, 'Mobitel')
    )
    member = models.ForeignKey(Member, verbose_name="član")
    contact = models.CharField("kontakt", max_length=64)
    contact_type = models.CharField('Tip', max_length=255, choices=TYPES, null=True)

    class Meta:
        verbose_name = "kontakt"
        verbose_name_plural = "kontakti"

    def __unicode__(self):
        return self.contact


class Address(models.Model):
    member = models.ForeignKey(Member, verbose_name="član")
    address = models.CharField("adresa", max_length=64)
    town = models.CharField("grad", default="Zagreb",
        max_length=32, null=True, blank=True)
    zipcode = models.CharField("poštanski broj",
        default="10000", max_length=16, null=True, blank=True)
    country = models.CharField("država", default="Hrvatska",
        max_length=32, null=True, blank=True)

    class Meta:
        verbose_name = "adresa"
        verbose_name_plural = "adrese"

    def __unicode__(self):
        return self.address
