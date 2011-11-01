# Create your views here.
from django.shortcuts import render_to_response
from datetime import datetime
from datetime import timedelta
from django.http import HttpResponse,HttpResponseRedirect
from django.db import connection
from django.template import RequestContext

from gallery.models import *
from django.db.models import Q

def show_gallery(request):
  return render_to_response('gallery_main.html', context_instance=RequestContext(request))

def list_albums(request, cat, year=datetime.today().year):

  years = Album.objects.filter(category=cat.upper()).dates('date_of_event', 'year', order='DESC')
  return render_to_response('gallery_spec.html', {
    'list': Album.objects.filter(category=cat.upper(), date_of_event__year=year).order_by('-date_of_event'),
    'years': years,
    'cat': cat,
    }, context_instance=RequestContext(request))

#show content of an album
def view_album(request, album_slug):
  album = Album.objects.get(slug = album_slug)
  category = album.category.lower()
  album_title = album.title
  date = album.date_of_event
  photographer = album.photographer
  description = album.description
  images = album.image_set.all()
  return render_to_response('gallery_view_album.html', { 'images' : images, 
    'category': category, 
    'album_title' : album_title,
    'photographer' : photographer,
    'description' : description,
    'date'    : date
    }, context_instance=RequestContext(request))



#show image
def view_image(request, image_slug):
  image = Image.objects.get(slug = image_slug)
  #return image.upload_path
  return render_to_response('gallery_view_image.html',{
  'image' : image
  })
  #return HttpResponseRedirect(image.upload_path)

