#coding: utf8

from django.shortcuts import render

from .forms import SearchForm


def search(request):
    """Returns results of search query on news & events."""

    news = []
    events = []

    form = SearchForm(request.GET or None)

    if form.is_valid():
        news, events = form.get_results()

    return render(request, 'search.html', {
            'form': form,
            'news': news,
            'events': events
        })
