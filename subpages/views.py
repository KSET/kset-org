from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from subpages.models import Subpage


def by_slug(request, slug='klub'):

    return render_to_response('club.html', {
        'subpage': Subpage.objects.get(slug=slug),
    }, context_instance=RequestContext(request))


def multimedia(request):
    """Renders multimedia subpage (which is static :-))."""

    return render_to_response('multimedia.html', {
        "active_menu": 'multimedia',
        }, context_instance=RequestContext(request))
    
