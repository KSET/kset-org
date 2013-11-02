#coding: utf8

from django.db import models

from tinymce.models import HTMLField


__all__ = ['Group', 'Member', 'Contact', 'ContactType', 'Address', 'MemberGroupLink']


class GroupManager(models.Manager):

    def tree(self, id=None):
        groups = self.filter(parent=id).order_by('name')

        if groups:
            for grp in groups:
                grp.childs = self.tree(grp.id)

        return groups


class Group(models.Model):
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
    card_id = models.CharField("iskaznica", max_length=32, null=True, blank=True)
    name = models.CharField("ime", max_length=32)
    surname = models.CharField("prezime", max_length=64)
    slug = models.SlugField()
    nickname = models.CharField("nadimak", max_length=32, null=True, blank=True)
    username = models.CharField("korisničko ime", unique=True, max_length=32)
    password = models.CharField("lozinka", max_length=32, null=True, blank=True)
    birth = models.DateField("datum rođenja", null=True, blank=True)
    death = models.DateField("datum smrti", null=True, blank=True)
    comment = HTMLField("komentar", null=True, blank=True)
    groups = models.ManyToManyField(Group, through='MemberGroupLink')
    image = models.ImageField(upload_to="/", null=True, blank=True, verbose_name="slika")
    objects = MemberManager()

    def division(self):
        """Returns division name. --> Hardcoded group ID!"""

        try:
            return MemberGroupLink.objects.filter(member=self.id).filter(group__parent=1).values('group__name')[0]["group__name"]
        except:
            return u'---'

    def card(self):
        """Returns card. --> Hardcoded group ID!"""

        try:
            return MemberGroupLink.objects.filter(member=self.id).filter(group__parent=2).values('group__name')[0]["group__name"]
        except:
            return u'---'

    class Meta:
        verbose_name = "član"
        verbose_name_plural = "članovi"

    def __unicode__(self):
        return self.name + " " + self.surname


class MemberGroupLink(models.Model):
    member = models.ForeignKey(Member, verbose_name="član")
    group = models.ForeignKey(Group, verbose_name="grupa")
    date_start = models.DateField("početak", null=True, blank=True)
    date_end = models.DateField("kraj", null=True, blank=True)

    class Meta:
        verbose_name = "članstvo"
        verbose_name_plural = "članstva"


### member contacts

class ContactType(models.Model):
    name = models.CharField("naziv", max_length=32)

    class Meta:
        verbose_name = "tip kontakta"
        verbose_name_plural = "tipovi kontakata"

    def __unicode__(self):
        return self.name


class Contact(models.Model):
    member = models.ForeignKey(Member, verbose_name="član")
    contact = models.CharField("kontakt", max_length=64)
    contact_type = models.ForeignKey(ContactType, verbose_name="tip")

    class Meta:
        verbose_name = "kontakt"
        verbose_name_plural = "kontakti"

    def __unicode__(self):
        return self.contact


class Address(models.Model):
    member = models.ForeignKey(Member, verbose_name="član")
    address = models.CharField("adresa", max_length=64)
    town = models.CharField("grad", default="Zagreb", max_length=32, null=True, blank=True)
    zipcode = models.CharField("poštanski broj", default="10000", max_length=16, null=True, blank=True)
    country = models.CharField("država", default="Hrvatska", max_length=32, null=True, blank=True)

    class Meta:
        verbose_name = "adresa"
        verbose_name_plural = "adrese"

    def __unicode__(self):
        return self.address
