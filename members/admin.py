#coding: utf-8

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import *
from actions import export_as_csv_action
from actions import make_bill


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
        ("Osobni podaci", {'fields': ['name', 'surname', 'nickname', 'gender', 'oib', 'birth',
                                        'death', 'join_date', 'leave_date', 'college',
                                      'college_confirmation', 'membership_paid', 'image', 'comment']}),
    ]
    list_display = ('username', 'name', 'surname', 'nickname', 'division', 'card')
    ordering = ('surname', 'name')
    search_fields = ('name', 'surname', 'nickname', 'username')
    search_fields_verbose = ('Ime', 'Prezime', 'Nadimak',)
    list_filter = ['groups']

    actions = [
        make_bill,
        export_as_csv_action(
            fields=[
                'name', 'surname', 'gender', 'oib', 'division', 'card', 'join_date',
                'leave_date', 'birth', 'address', 'phone', 'mobile', 'email', 'college']
        )
    ]
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
