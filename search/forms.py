# -*- coding: utf-8 -*-

from django import forms

from events.models import Event
from news.models import News


class SearchForm(forms.Form):
    query = forms.CharField(max_length=64)

    def clean_query(self):
        if len(self.cleaned_data['query']) < 3:
            raise forms.ValidationError(
                'Neispravan unos! (za pretragu su potrebna minimalno 3 znaka!)')
        return self.cleaned_data['query']

    def get_results(self):
        news = News.objects.filter(
            subject__icontains=self.cleaned_data['query']).order_by('-created_at')
        events = Event.objects.filter(
            title__icontains=self.cleaned_data['query']).order_by('-date')

        return news, events
