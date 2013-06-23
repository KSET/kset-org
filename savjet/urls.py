from django.conf.urls import *
from kset.savjet.models import Post

urlpatterns = patterns('django.views.generic.date_based',
    (r'^$', 'archive_index', {
        'queryset': Post.objects.all(),
        'date_field': 'date'}),
)
