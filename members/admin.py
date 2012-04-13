#coding: utf-8

from datetime import datetime
import md5

from django.contrib import admin
from django import forms
from django.utils.encoding import smart_str

from members.models import *
from members.membership import InvoiceTemplate


def make_bill(modeladmin, request, queryset):
    """Creates bill (.pdf) with memberships"""

    bill = InvoiceTemplate("/var/www/py/kset/media/uploads/invoice.pdf")

    odd = True
    for member in queryset:
        bill.buyer['name'] = smart_str(member.name + " " + member.surname)
        
        bill.info['num'] = "2010-1"
        bill.info['date'] = datetime.now().strftime("%d.%m.%Y.")
        bill.info['items'] = [['članarina za SSFER', 100.0]]

        bill.populate()
        bill.hr()

        if not odd:
            odd = True
            bill.newPage()
        else:
            odd = False
    
    bill.create()

make_bill.short_description = "Ispisi clanarine"


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
    actions = [make_bill]

    form = MemberForm

    class Media:
        js = ('/media/static/tiny_mce/tiny_mce.js',)

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
