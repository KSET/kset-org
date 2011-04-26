#coding: utf8

from django.shortcuts import render_to_response
from django.template import RequestContext

from members.models import Member, Address


def red(request):
    """Print out in html red members addresses."""

    members = Member.objects.filter(groups__id=16).exclude(death__isnull=False).order_by('surname', 'name')

    for member in members:
        member.addresses = Address.objects.filter(member=member.id)

    return render_to_response('members-red.html', {
        'members': members,
        })
