#coding: utf8

from django.contrib import admin
from members.models import *

from django import forms

import md5

class MemberForm( forms.ModelForm ):
    resetpw = forms.CharField(widget=forms.PasswordInput, label="Lozinka", required=False)
    resetpw2 = forms.CharField(widget=forms.PasswordInput, label="Ponovi lozinku", required=False)

    class Meta:
        model = Member


##
## Majke li mu!!!
## U zadnje polje ne postavi dobar ID od 'input' taga.
## Mislim da je problem do Javascripta i Grappellia.
## Ugl podatak upisan u zadnje polje Inline forme se neće upisati u bazu.
##

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
    list_display = ('name', 'surname', 'nickname', 'division', 'card', ) #'active'
    ordering = ('surname','name')
    search_fields = ('name', 'surname', 'nickname',)
    search_fields_verbose = ('Ime', 'Prezime', 'Nadimak',)
    list_filter = ['groups']
    inlines = (MemberAddress, MemberContact, MemberGroup, )

    form = MemberForm

    class Media:
        js = ('admin/tinymce/jscripts/tiny_mce/tiny_mce.js','admin/tinymce_setup/tinymce_description.js',)

    def save_model(self, request, obj, form, change):

        if ( len(form['resetpw'].data) == 0):
            if (change):
                obj.password = Member.objects.get(username=request.POST["username"]).password
            else:
                obj.password = "!"
        else:
            if ( len(form['resetpw'].data) >= 5  and form['resetpw'].data == form['resetpw2'].data):
                obj.password = md5.new(form['resetpw'].data).hexdigest()
            
        obj.save()


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug')
    ordering = ('parent', 'name')


admin.site.register(Group, GroupAdmin)
admin.site.register(Member,MemberAdmin)
admin.site.register(ContactType)
