# -*- coding: utf-8 -*-

from django import forms

from .models import Subscription


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription

    def clean_email(self):
        if Subscription.objects.filter(email=self.cleaned_data.get('email')):
            raise forms.ValidationError('Email adresa je već pretplaćena.')
        return self.cleaned_data.get('email')
