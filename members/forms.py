#coding: utf8
import hashlib

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.conf import settings

from .models import Member


__all__ = ['LoginForm', 'MemberCreationForm', 'MemberChangeForm']


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=32)
    password = forms.CharField(widget=forms.PasswordInput,
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
