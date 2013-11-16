import calendar as cal
from datetime import date, datetime, timedelta

from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import Event


def by_slug(request, slug):
    event = get_object_or_404(Event, slug=slug)
    return render(request, 'event.html', {'event': event})


def by_date(request, date):
    events = Event.objects.filter(date=date)
    return render(request, 'events.html', {'events': events})


def archive(request, year=datetime.today().year):
    # get distinct years
    years = Event.objects.dates('date', 'year', order='DESC')

    events = Event.objects.filter(date__year=year).order_by('-date')

    return render(request, 'events-archive.html',
        {'events': events, 'years': years})


def newsletter(request):
    """
    Renders html for newsletter.
    Start + end dates are passed by GET.
    """
    from_date = request.GET.get('from')
    till_date = request.GET.get('till')

    if from_date and till_date:
        from_date = datetime.strptime(from_date, '%Y-%m-%d')
        till_date = datetime.strptime(till_date, '%Y-%m-%d')
    else:
        from_date = date(date.today().year, date.today().month, 1)
        till_date = from_date + timedelta(days=31)

    events = Event.objects.filter(date__gte=from_date).filter(date__lte=till_date).order_by('date')

    return render(request, 'newsletter.html',
        {'from_date': from_date, 'till_date': till_date, 'events': events})


def calendar(request):
    """
    Renders calendar for events (dates & styles).
    First checks for year+month in POST request, else takes current year+month.
    """

    def cal_date_add_style(date):
        """Applies css styles for given date."""

        style = ""

        if date.month != current_date.month:
            style += 'out-month '

        if Event.objects.is_reserved(date):
            style += 'reserved '

        if date == date.today():
            style += 'today '

        return (date, style)

    # try POST data, otherwise use current year-month
    ## FIXME: Use a form here not raw POST data
    try:
        current_date = date(int(request.POST.get('year')),
            int(request.POST.get('month')), 1)
    except TypeError:
        current_date = date(date.today().year, date.today().month, 1)

    # set prev/next year-month for calendar navigation
    previous_date = current_date - timedelta(days=1)
    next_date = current_date + timedelta(days=31)

    # prepares dates+styles for calendar
    _cal = cal.Calendar()
    cal_dates = _cal.itermonthdates(current_date.year, current_date.month)
    cal_dates = map(cal_date_add_style, cal_dates)

    return render(request, 'calendar.html', {
        'dates': cal_dates, 'previous_date': previous_date,
        'current_date': current_date, 'next_date': next_date})


def events_rdf(request):
    """ Returns Rss1.0 (rdf). """

    events_list = Event.objects.filter(date__gte=datetime.now()).order_by('date')

    return render(request, 'feeds/rdf.html',
        {'events': events_list}, mimetype="application/xml")
