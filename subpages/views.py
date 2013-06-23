from django.shortcuts import render, get_object_or_404

from .models import Subpage


def by_slug(request, slug='klub'):

    subpage = get_object_or_404(Subpage, slug=slug)

    return render(request, 'club.html', {
        'subpage': subpage,
    })


def multimedia(request):
    """Renders multimedia subpage (which is static :-))."""

    return render(request, 'multimedia.html', {
        "active_menu": 'multimedia',
    })
