#coding: utf8

from django import forms

import md5

class LoginForm(forms.Form):
    username = forms.CharField(label="Korisničko ime:", max_length=32)
    password = forms.CharField(widget=forms.PasswordInput, label="Lozinka:", max_length=32)

    def clean(self):

        data = self.cleaned_data

        try:
            member = Member.objects.get(password=md5.new(data["password"]).hexdigest(),
                                        username=data["username"])
        except:
            raise forms.ValidationError(u'Pogrešno korisničko ime ili lozinka!')

        return data


class EditProfileForm(forms.Form):
    pw = forms.CharField(widget=forms.PasswordInput, label="Lozinka:", max_length=32)
    pw2 = forms.CharField(widget=forms.PasswordInput, label="Ponovi lozinku:", max_length=32)

   
