# -*- coding: utf-8 -*-

from django import forms

from .models import Subscription
from django.utils.translation import ugettext_lazy as _

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription

    def clean_email(self):
        if not self.cleaned_data.get('email'):
            # Translators: Molimo unesite email adresu.
            raise forms.ValidationError(_('newsletter.subscription.no-email'))
        if Subscription.objects.filter(email=self.cleaned_data.get('email')):
            # Translators: Email adresa je već pretplaćena.
            raise forms.ValidationError(_('newsletter.subscription.not-unique-email'))
        return self.cleaned_data.get('email')
