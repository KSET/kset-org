from django import forms

from .models import Event


class EventAdminForm(forms.ModelForm):
    class Meta:
        model = Event

    def clean_tags(self):
        cleaned_tags = []
        tags = self.cleaned_data.get('tags')

        # Remove empty tags if trailing comma and remove white space
        for tag in tags:
            if tag:
                cleaned_tags.append(tag.strip())

        return cleaned_tags
