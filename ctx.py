from datetime import datetime
import os
import random

from django.conf import settings

from events.models import Event
from subpages.models import Subpage


def header(request):

    ctx = {}

    try:
        files = os.listdir(os.path.join(settings.STATIC_ROOT, 'frontend', 'images', 'headers'))
        ctx['header_bg'] = random.choice(files)
    except Exception as e:
        pass

    ctx['header_events'] = Event.objects.filter(date__gte=datetime.now()).order_by('date')

    if request.path[1:].split('/')[0] == 'klub':
        try:
            ctx['divisions'] = Subpage.objects.filter(category__slug='sekcije').order_by('title')
            ctx['leaders'] = Subpage.objects.get(slug='voditelji')
            ctx['projects'] = Subpage.objects.filter(category__slug='projekti').order_by('title')
        except:
            pass

    return ctx
