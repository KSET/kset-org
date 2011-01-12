#coding: utf8

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from datetime import datetime

from news.models import News
from events.models import Event


def active(request):
    """Renders default/program template:
       - The list of all active (published and not yet expired) news,
    """

    news = News.objects.exclude(publish__gte=datetime.now()).exclude(expire__lte=datetime.now()).order_by('-publish') 
    events = Event.objects.filter(date__gte=datetime.now()).filter(announce=True).order_by('date')[:3]
 
    return render_to_response('news.html', {
        'news': news,
        'events': events,
        }, context_instance=RequestContext(request))


def by_slug(request, slug):

    return render_to_response('news-item.html', {
        'news': News.objects.get(slug=slug),
        }, context_instance=RequestContext(request))


def archive(request):

    return render_to_response('news-archive.html', {
        'news': News.objects.order_by('-publish'),
        }, context_instance=RequestContext(request))

