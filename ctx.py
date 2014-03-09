from datetime import datetime
import os
import random

from django.conf import settings

from events.models import Event


def header(request):

    ctx = {}

    try:
        files = os.listdir(os.path.join(settings.STATIC_ROOT, 'frontend', 'images', 'headers'))
        ctx['header_bg'] = random.choice(files)
    except Exception as e:
        pass

    ctx['header_events'] = Event.objects.filter(date__gte=datetime.now()).order_by('date')
    try:
        if ctx['header_events'][0].date == datetime.now().date():
            ctx['today_active'] = True
    except:
        pass

    return ctx


def baseurl(request):
    if request.is_secure():
        scheme = 'https://'
    else:
        scheme = 'http://'

    return {'BASE_URL': scheme + request.get_host(),}
