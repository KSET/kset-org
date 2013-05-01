#coding: utf8
from datetime import datetime, timedelta

from django.shortcuts import render, get_object_or_404

from .models import News
from events.models import Event
from gallery.models import Album


def active(request):
    """
    Renders default/program template:
    The list of all active (published and not yet expired) news,
    """

    news = News.get_frontpage_news()
    events = Event.get_frontpage_events()
    daytime_events = Event.get_frontpage_daytime_events()

    sticky_news = News.get_sticky_news()

    #get latest albums from gallery
    latest = Album.objects.filter(category='LIVE',
        date_of_event__range=(datetime.today() - timedelta(14), datetime.today())).order_by('-date_of_event')[:3]

    return render(request, 'news.html',
        {'news': news, 'events': events, 'daytime_events': daytime_events,
        'latest': latest, 'sticky_news': sticky_news})


def by_slug(request, slug):
    news = get_object_or_404(News, slug=slug)
    return render(request, 'news-item.html', {'news': news})


def archive(request):
    news = News.objects.order_by('-created_at')
    return render(request, 'news-archive.html', {'news': news})
