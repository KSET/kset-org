#coding: utf8
import hashlib

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.conf import settings

from .models import Member, Group, Contact, ResetPasswordLink, Address
from .helpers import send_template_email


__all__ = ['LoginForm', 'MemberCreationForm', 'MemberChangeForm', 'MemberFilterForm',
    'MemberForgotPasswordForm', 'ResetPasswordForm', 'AddAddressForm', 'AddContactForm',
    'ChangePasswordForm']


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=32,
        widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        label="Password",
        max_length=32)

    def clean(self):

        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if not username or not password:
            raise forms.ValidationError('Username and Password fields are required.')

        try:
            self.cleaned_data['member'] = Member.objects.get(
                password=hashlib.md5(password+settings.SECRET_KEY).hexdigest(),
                username=username).id

        except Member.DoesNotExist:
            raise forms.ValidationError(u'Pogrešno korisničko ime ili lozinka!')

        return self.cleaned_data


class MemberCreationForm(forms.ModelForm):
    """
    A form for creating new member. Includes all the
    required fields, plus a repeated password.
    """
    class Meta:
        model = Member

    password1 = forms.CharField(label="Lozinka", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Ponovi Lozinku", widget=forms.PasswordInput)

    fields = ("username",)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            msg = "Passwords don't match"
            raise forms.ValidationError(msg)
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        member = super(MemberCreationForm, self).save(commit=False)
        member.set_password(self.cleaned_data["password1"])
        if commit:
            member.save()
        return member


class MemberChangeForm(forms.ModelForm):
    """
    A form for updating member info. Includes all the fields
    on the member, but replaces the password field with
    admin"s password hash display field.
    """
    class Meta:
        model = Member

    password = ReadOnlyPasswordHashField(help_text=("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))

    def clean_password(self):
        # Regardless of what the user provides, return the
        # initial value. This is done here, rather than on
        # the field, because the field does not have access
        # to the initial value
        return self.initial["password"]


class MemberFilterForm(forms.Form):
    division = forms.ModelChoiceField(
        queryset=Group.objects.filter(parent__name=Group.DIVISION).order_by('name'),
        empty_label='Sekcija',
        required=False)
    card = forms.ModelChoiceField(
        queryset=Group.objects.filter(parent__name=Group.CARD).order_by('name'),
        empty_label='Iskaznica',
        required=False)
    status = forms.ModelChoiceField(
        queryset=Group.objects.filter(parent__name=Group.STATUS).order_by('name'),
        empty_label='Status',
        required=False)

    def filter(self):
        self.is_valid()  # force validation just in case
        division = self.cleaned_data.get('division')
        card = self.cleaned_data.get('card')
        status = self.cleaned_data.get('status')

        # This will build the query based on supplied filters
        # NOTE: it executes just one query at the end
        members = Member.objects.all()
        if division:
            members = members.filter(groups=division)
        if card:
            members = members.filter(groups=card)
        if status:
            members = members.filter(groups=status)

        return members.order_by('surname', 'name')


class MemberForgotPasswordForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        member_id = None
        if email:
            member_contacts = Contact.objects.filter(
                contact_type=Contact.TYPE_EMAIL).values('contact', 'member_id')
            found_contacts = [c for c in member_contacts if c['contact'] == email]

            # We need to match exactly *one*) contact
            if len(found_contacts) != 1:
                raise forms.ValidationError('Nije pronađen član sa navedenom email adresom.')
            member_id = found_contacts[0]['member_id']
        return email, member_id

    def send_password_reset_email(self):
        member_email, member_id = self.cleaned_data['email']
        member = Member.objects.get(id=member_id)

        # delete all existing reset request
        ResetPasswordLink.objects.filter(member=member).delete()

        # create new reset link
        rpl = ResetPasswordLink.objects.create(member=member)

        send_template_email(
            member_email=member_email,
            member_name=member.name,
            reset_password_link=rpl.unique_link)


class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(
        label='Nova Lozinka',
        widget=forms.PasswordInput())
    password2 = forms.CharField(
        label='Ponovite Lozinku',
        widget=forms.PasswordInput())

    def clean(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 != p2:
            raise forms.ValidationError('Upisane lozinke se moraju podudarati.')
        if len(p1) < 8:
            raise forms.ValidationError('Molimo unesite lozinku od najmanje 8 znakova.')
        return self.cleaned_data

    def set_new_password(self, rpl):
        member = rpl.member
        member.set_password(self.cleaned_data['password1'])
        member.save()
        rpl.delete()


class ChangePasswordForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.member = kwargs.pop('member')
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    current = forms.CharField(
        label='Trenutna lozinka',
        widget=forms.PasswordInput(attrs={'placeholder': 'Trenutna Lozinka'}))
    password1 = forms.CharField(
        label='Nova Lozinka',
        widget=forms.PasswordInput(attrs={'placeholder': 'Nova Lozinka'}))
    password2 = forms.CharField(
        label='Ponovite Lozinku',
        widget=forms.PasswordInput(attrs={'placeholder': 'Ponovite Lozinku'}))

    def clean(self):
        current = self.cleaned_data.get('current')
        hashed = self.member.hash_password(current)
        if hashed != self.member.password:
            raise forms.ValidationError('Unijeli ste neispravnu lozinku.')
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 != p2:
            raise forms.ValidationError('Upisane lozinke se moraju podudarati.')
        if len(p1) < 8:
            raise forms.ValidationError('Molimo unesite lozinku od najmanje 8 znakova.')
        return self.cleaned_data

    def set_new_password(self):
        self.member.set_password(self.cleaned_data['password1'])
        self.member.save()


class AddAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ('member',)


class AddContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ('member',)
