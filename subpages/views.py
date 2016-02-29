# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _


DIVISIONS = [
    {
        'name': _("bike-title"),
        'id': 'bike',
        'logo': '/static/frontend/images/divisions/bike_resized.jpg'
    },
    {
        'name': _("disco-title"),
        'id': 'disco',
        'logo': '/static/frontend/images/divisions/disco_resized.jpg'
    },
    {
        'name': _("drama-title"),
        'id': 'drama',
        'logo': '/static/frontend/images/divisions/drama_resized.jpg'
    },
    {
        'name': _("foto-title"),
        'id': 'foto',
        'logo': '/static/frontend/images/divisions/foto_resized.jpg'
    },
    {
        'name': _("music-title"),
        'id': 'music',
        'logo': '/static/frontend/images/divisions/music_resized.jpg'
    },
    {
        'name': _("pi-title"),
        'id': 'pijandure',
        'logo': '/static/frontend/images/divisions/pijandure_resized.jpg'
    },
    {
        'name': _("comp"),
        'id': 'comp',
        'logo': '/static/frontend/images/divisions/comp_resized.jpg'
    },
    {
        'name': _("tech-title"),
        'id': 'tech',
        'logo': '/static/frontend/images/divisions/tech_resized.jpg'
    },
    {
        'name': _("video-title"),
        'id': 'video',
        'logo': '/static/frontend/images/divisions/video_resized.jpg'
    }
]

PROJECTS = [
    {
        'name': _("mono-title"),
        'id': 'monografija',
        'logo': '/static/frontend/images/projects/monografija_resized.jpg'
    },
    {
        'name': _("powertrip-title"),
        'id': 'powertrip',
        'logo': '/static/frontend/images/projects/powertrip_resized.jpg'
    },
    {
        'name': _("rally-title"),
        'id': 'rally',
        'logo': '/static/frontend/images/projects/rally_resized.jpg'
    }
]


def club(request):
    return render(request, 'club.html', {
        'divisions': DIVISIONS,
        'projects': PROJECTS
        })


def division(request, division):
    template = 'divisions/{0}.html'.format(division)
    return render(request, template, {
        'divisions': DIVISIONS,
        'projects': PROJECTS
    })


def project(request, project):
    template = 'projects/{0}.html'.format(project)
    return render(request, template, {
        'divisions': DIVISIONS,
        'projects': PROJECTS
    })


def multimedia(request):
    """Renders multimedia subpage"""

    return render(request, 'multimedia.html', {
        "active_menu": 'multimedia',
    })


def alumni(request):
    """Renders alumni subpage"""

    return render(request, 'alumni.html', {
        'divisions': DIVISIONS,
        'projects': PROJECTS
    })
