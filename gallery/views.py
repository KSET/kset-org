from datetime import datetime

from django.shortcuts import render, get_object_or_404

from .models import Image, Album


def show_gallery(request):
    return render(request, 'gallery_main.html')


def list_albums(request, category, year=datetime.today().year):
    years = Album.objects.filter(
        category=category).dates(
        'date_of_event', 'year', order='DESC')

    if category == 'foto':
        albums = Album.objects.filter(
            category=category).order_by('-date_of_event')
    else:
        albums = Album.objects.filter(category=category,
            date_of_event__year=year).order_by('-date_of_event')

    return render(request, 'gallery_spec.html', {
        'albums': albums,
        'years': years,
        'active_year': str(year) + '.',
        'category': category
    })


def view_album(request, category, album_slug):
    album = get_object_or_404(Album, slug=album_slug)
    category = album.category
    images = album.images.order_by('title')

    return render(request, 'gallery_view_album.html',
        {'images': images, 'category': category, 'album': album})


def view_image(request, category, album_slug, image_slug):
    image = get_object_or_404(Image, slug=image_slug)
    return render(request, 'gallery_view_image.html', {'image': image})
