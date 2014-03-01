# -*- coding: utf-8 -*-

from itertools import chain

from django import forms
from django.db.models import Q

from djorm_expressions.base import SqlExpression

from events.models import Event
from news.models import News


def flatten(list_of_lists):
    "Flatten one level of nesting"
    return chain.from_iterable(list_of_lists)


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

        query_string_args = self.cleaned_data['query'].split(':')

        if query_string_args[0] == 'tags':
            tags = map(lambda t: t.strip(), flatten(map(lambda t: t.split(','), query_string_args[1:])))
            events = Event.objects.where(SqlExpression("tags", "@>", tags))
        else:
            events = Event.objects.filter(
                title__icontains=self.cleaned_data['query']).order_by('-date')

        return news, events
