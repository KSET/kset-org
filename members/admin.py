#coding: utf-8

import os

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.conf import settings
from django.utils.encoding import smart_str

from .models import *
from .forms import *
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


class MemberAdmin(UserAdmin):
    add_form_template = 'admin/auth/user/add_form.html'
    change_user_password_template = None
    add_form = MemberCreationForm
    form = MemberChangeForm

    fieldsets = [
        ("Korisnički račun", {'fields': ['username', 'password']}),
        ("Osobni podaci", {'fields': ['name', 'surname', 'nickname', 'birth',
                                        'death', 'image', 'comment']}),
    ]
    list_display = ('username', 'name', 'surname', 'nickname', 'division', 'card', )
    ordering = ('surname', 'name')
    search_fields = ('name', 'surname', 'nickname', 'username')
    search_fields_verbose = ('Ime', 'Prezime', 'Nadimak',)
    list_filter = ['groups']

    actions = [make_bill]
    filter_horizontal = ()

    add_fieldsets = (
        (None, {"classes": ("wide",),
        "fields": ("username", "password1", "password2")}),
    )

    def get_fieldsets(self, request, obj=None):
        self.inlines = ()
        if not obj:
            return self.add_fieldsets
        else:
            self.inlines = (MemberAddress, MemberContact, MemberGroup, )
        return super(MemberAdmin, self).get_fieldsets(request, obj)


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug')
    ordering = ('parent', 'name')


admin.site.register(Group, GroupAdmin)
admin.site.register(Member, MemberAdmin)
