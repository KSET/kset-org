#coding: utf8

from django.shortcuts import render_to_response
from django.template import RequestContext

from members.models import Member


def list(request):
    """ ... """

    return render_to_response('members.html', {
        'members', Member.objects.all().order_by('-surname', '-name'),
        }, context_instance=RequestContext(request))


