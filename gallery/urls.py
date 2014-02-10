from django.conf.urls import patterns, url

urlpatterns = patterns('gallery.views',
    url(r'^$', 'show_gallery',
        name='gallery_index'),
    url(r'^(?P<category>\w+)/$', 'list_albums',
        name='gallery_category_albums'),
    url(r'^(?P<category>\w+)/(?P<year>\d{4})/$', 'list_albums',
        name='gallery_category_albums_by_year'),
    url(r'^(?P<category>\w+)/(?P<album_slug>[-_a-zA-Z0-9]+)/$', 'view_album',
        name='gallery_view_album'),
    url(r'^(?P<category>\w+)/(?P<album_slug>[-_a-zA-Z0-9]+)/(?P<image_slug>[-_a-zA-Z0-9]+)/$', 'view_image',
        name='gallery_view_image'),
)
