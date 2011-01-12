from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db import connection

from datetime import date
import datetime
import calendar as cal

from events.models import Event


def by_slug(request, slug):

    return render_to_response('event.html', {
        'event': Event.objects.get(slug=slug),
        }, context_instance=RequestContext(request))

def by_date(request, date):

    return render_to_response('events.html', {
        'events': Event.objects.filter(date=date),
        }, context_instance=RequestContext(request))


def archive(request, year=datetime.datetime.today().year):

    # get distinct years
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT to_char(date, 'YYYY') AS year FROM events_event ORDER BY year DESC;")
    years = cursor.fetchall()

    return render_to_response('events-archive.html', {
        'events': Event.objects.filter(date__year=year).order_by('-date'),
        'years': years,
        }, context_instance=RequestContext(request))


def newsletter(request):
    """Renders html for newsletter.
       Start + end dates are passed by GET.
    """

    # try GET
    try:
        fromDate = datetime.datetime.strptime(request.GET.get("from"), '%Y-%m-%d')
        tillDate = datetime.datetime.strptime(request.GET.get("till"), '%Y-%m-%d')

    except:
        fromDate = datetime.date( date.today().year, date.today().month, 1)
        tillDate = fromDate + datetime.timedelta(days = 31)

    events = Event.objects.filter(date__gte=fromDate).filter(date__lte=tillDate).order_by('date')

    return render_to_response('newsletter.html', {
        'fromDate': fromDate,
        'tillDate': tillDate,
        'events': events
        })


def calendar(request):
    """Renders calendar for events (dates & styles).
       First checks for year+month in POST request, else takes current year+month."""

    def cal_date_add_style(date):
        """Applies css styles for given date."""
        
        style = ""

        if date.month != current_date.month: style += 'out-month '

        if Event.objects.is_reserved(date): style += 'reserved '

        if date == date.today(): style += 'today '

        return (date, style)


    # try POST data, otherwise use current year-month
    try:
        current_date = datetime.date( int(request.POST.get('year')), int(request.POST.get('month')), 1)
    except:
        current_date = datetime.date( date.today().year, date.today().month, 1)


    # set prev/next year-month for calendar navigation
    previous_date = current_date - datetime.timedelta(days = 1)
    next_date = current_date + datetime.timedelta(days = 31)

    # prepares dates+styles for calendar
    _cal = cal.Calendar()
    cal_dates = _cal.itermonthdates( current_date.year, current_date.month )    
    cal_dates = map(cal_date_add_style, cal_dates)

 
    return render_to_response('calendar.html', {
        'dates': cal_dates,
        'previous_date': previous_date, 
        'current_date': current_date,
        'next_date': next_date,
        })



# veljko @ 2009-11-24 - samo za Jagya ;-)
def events_rdf(request):
    """Returns Rss1.0 (rdf)."""

    events_list = Event.objects.filter(date__gte=datetime.datetime.now()).order_by('date')
    
    return render_to_response('feeds/rdf.html', {
        'events': events_list,
        },mimetype="application/xml")
            
