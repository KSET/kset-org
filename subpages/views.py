from django.shortcuts import render

from .models import Subpage


def by_slug(request, slug='klub'):

    return render(request, 'club.html', {
        'subpage': Subpage.objects.get(slug=slug),
    })


def multimedia(request):
    """Renders multimedia subpage (which is static :-))."""

    return render(request, 'multimedia.html', {
        "active_menu": 'multimedia',
    })
