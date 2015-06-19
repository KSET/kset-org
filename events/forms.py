from django import forms

from .models import Event

import re


class EventAdminForm(forms.ModelForm):
    class Meta:
        model = Event

    def clean_tags(self):
        cleaned_tags = []
        tags = self.cleaned_data.get('tags')

        # Remove empty tags if trailing comma and remove white space
        for tag in tags:
            if tag:
                cleaned_tags.append(tag.strip().lower())

        return cleaned_tags

    def clean_fbeventid(self):
        fbeventid = self.cleaned_data.get('fbeventid')

        return  re.sub("[^0-9]", "", fbeventid)
