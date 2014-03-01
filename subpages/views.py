# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404


DIVISIONS = [
    {
        'name': 'Bike',
        'id': 'bike',
        'logo': '/static/frontend/images/divisions/bike_resized.jpg'
    },
    {
        'name': 'Disco',
        'id': 'disco',
        'logo': '/static/frontend/images/divisions/disco_resized.jpg'
    },
    {
        'name': 'Dramska',
        'id': 'drama',
        'logo': '/static/frontend/images/divisions/drama_resized.jpg'
    },
    {
        'name': 'Foto',
        'id': 'foto',
        'logo': '/static/frontend/images/divisions/foto_resized.jpg'
    },
    {
        'name': 'Glazbena',
        'id': 'music',
        'logo': '/static/frontend/images/divisions/music_resized.jpg'
    },
    {
        'name': 'Pijandure',
        'id': 'pijandure',
        'logo': '/static/frontend/images/divisions/pijandure_resized.jpg'
    },
    {
        'name': 'Računarska',
        'id': 'comp',
        'logo': '/static/frontend/images/divisions/comp_resized.jpg'
    },
    {
        'name': 'Tehnička',
        'id': 'tech',
        'logo': '/static/frontend/images/divisions/tech_resized.jpg'
    },
    {
        'name': 'Video',
        'id': 'video',
        'logo': '/static/frontend/images/divisions/video_resized.jpg'
    }
]

PROJECTS = [
    {
        'name': 'Monografija 2^5',
        'id': 'monografija',
        'logo': '/static/frontend/images/projects/monografija_resized.jpg'
    },
    {
        'name': 'PowerTrip',
        'id': 'powertrip',
        'logo': '/static/frontend/images/projects/powertrip_resized.jpg'
    },
    {
        'name': 'Rally',
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
