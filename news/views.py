#coding: utf8

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from datetime import datetime

from news.models import News
from events.models import Event

from gallery.models import Album
from datetime import timedelta
from datetime import datetime
from django.db.models import Q


def active(request):
    """Renders default/program template:
       - The list of all active (published and not yet expired) news,
    """

    news = News.objects.filter(created_at__range=(datetime.today() - timedelta(60), datetime.today())).order_by('-created_at')[:3]
    events = Event.objects.filter(date__gte=datetime.now()).filter(announce=True).order_by('date')[:3]
    daytime_events = Event.objects.filter(date__gte=datetime.now()).filter(announce=True, daytime=True).order_by('date')[:3]

    sticky_news = News.objects.filter(sticky=True).order_by('-created_at')

    #get latest albums from gallery
    latest = Album.objects.filter(category='LIVE',
        date_of_event__range=(datetime.today() - timedelta(14), datetime.today())).order_by('-date_of_event')[:3]

    return render_to_response('news.html', {
        'news': news,
        'events': events,
        'daytime_events': daytime_events,
        'latest': latest,
        'sticky_news': sticky_news
        }, context_instance=RequestContext(request))


def by_slug(request, slug):

    return render_to_response('news-item.html', {
        'news': News.objects.get(slug=slug),
        }, context_instance=RequestContext(request))


def archive(request):

    return render_to_response('news-archive.html', {
        'news': News.objects.order_by('-created_at'),
        }, context_instance=RequestContext(request))

