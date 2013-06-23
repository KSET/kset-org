#coding: utf-8

import hashlib
import os

from django.contrib import admin
from django.conf import settings
from django import forms
from django.utils.encoding import smart_str

from .models import *
from .membership import InvoiceTemplate


def make_bill(modeladmin, request, queryset):
    """Creates bill (.pdf) with memberships"""

    bill = InvoiceTemplate(os.path.join(settings.MEDIA_ROOT, 'uploads', 'invoice.pdf'))

    odd = True
    cnt = 437
    for member in queryset:
        bill.buyer['name'] = smart_str(member.name + " " + member.surname)
        bill.buyer['taxnum'] = member.id

        bill.info['num'] = "2011-" + str(cnt)
        bill.info['date'] = "04.01.2011."
        bill.info['items'] = [['članarina za SSFER', 100.0]]

        bill.populate()

        cnt = cnt + 1

        bill.newPage()

    bill.create()

make_bill.short_description = "Ispisi clanarine"


class MemberForm(forms.ModelForm):
    resetpw = forms.CharField(
        widget=forms.PasswordInput,
        label="Lozinka",
        required=False)
    resetpw2 = forms.CharField(
        widget=forms.PasswordInput,
        label="Ponovi lozinku",
        required=False)

    class Meta:
        model = Member


class MemberGroup(admin.TabularInline):
    model = MemberGroupLink
    fk_name = "member"
    extra = 1
    # Grappelli features
    classes = ('collapse-open',)
    #allow_add = True


class MemberAddress(admin.TabularInline):
    model = Address
    fk_name = "member"
    extra = 1
    # Grappelli features
    classes = ('collapse-open',)
    #allow_add = True


class MemberContact(admin.TabularInline):
    model = Contact
    fk_name = "member"
    extra = 1
    # Grappelli features
    classes = ('collapse-open',)
    #allow_add = True


class MemberAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Korisnički račun", {'fields': ['username', 'resetpw', 'resetpw2']}),
        ("Osobni podaci", {'fields': ['name', 'surname', 'nickname', 'birth', 'death', 'image', 'comment']}),
    ]
    list_display = ('name', 'surname', 'nickname', 'division', 'card', )
    ordering = ('surname', 'name')
    search_fields = ('name', 'surname', 'nickname',)
    search_fields_verbose = ('Ime', 'Prezime', 'Nadimak',)
    list_filter = ['groups']
    inlines = (MemberAddress, MemberContact, MemberGroup, )
    actions = [make_bill]

    form = MemberForm

    class Media:
        js = ('admin/tinymce/jscripts/tiny_mce/tiny_mce.js', 'admin/tinymce_setup/tinymce_description.js',)

    def save_model(self, request, obj, form, change):

        if (len(form['resetpw'].data) == 0):
            if (change):
                obj.password = Member.objects.get(username=request.POST["username"]).password
            else:
                obj.password = "!"
        else:
            if (len(form['resetpw'].data) >= 5 and form['resetpw'].data == form['resetpw2'].data):
                obj.password = hashlib.md5(form['resetpw'].data).hexdigest()

        obj.save()


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug')
    ordering = ('parent', 'name')


admin.site.register(Group, GroupAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(ContactType)
