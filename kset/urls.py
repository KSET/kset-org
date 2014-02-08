from django.conf.urls import url, patterns, include
from django.contrib import admin
from django.conf import settings

from feed import RssProgramFeed, AtomProgramFeed
from filebrowser.sites import site

admin.autodiscover()

urlpatterns = patterns('',

    # feeds
    url(r'^feeds/rss/$', RssProgramFeed(),
        name='feed_rss'),
    url(r'^feeds/atom/$', AtomProgramFeed(),
        name='feed_atom'),

    # news - homepage
    url(r'^$', 'news.views.active',
        name='index'),
    url(r'^arhiva/vijesti/', 'news.views.archive',
        name='news_archive'),
    url(r'^vijest/(?P<slug>[-a-zA-Z0-9]+)/$', 'news.views.by_slug',
        name='news_slug'),

    # events
    url(r'^arhiva/dogadaji/(?P<year>\d{4})/', 'events.views.archive',
        name='events_archive_year'),
    url(r'^arhiva/dogadaji/', 'events.views.archive',
        name='events_archive'),
    url(r'^dogadaj/(?P<slug>[-a-zA-Z0-9]+)/$', 'events.views.by_slug',
        name='event_slug'),
    url(r'^kalendar/$', 'events.views.calendar',
        name="calendar"),
    url(r'^dogadaji/(?P<date>[-0-9]+)/$', 'events.views.by_date',
        name='events_date'),


    # newsletter
    url(r'^newsletter/$', 'events.views.newsletter',
        name='newsletter'),
    url(r'^subscribe/$', 'newsletter.views.subscribe',
        name='subscribe'),

    # search
    url(r'^trazi/$', 'search.views.search',
        name='search'),

    url(r'^klub/sekcije/(?P<slug>[-a-zA-Z0-9]+)/$', 'subpages.views.by_slug',
        name='subpage_slug'),
    url(r'^klub/alumni/$', 'subpages.views.by_slug', {'slug': 'alumni'},
        name='alumni'),
    url(r'^klub/$', 'subpages.views.by_slug',
        name='club'),


    url(r'^multimedia/$', 'subpages.views.multimedia',
        name='multimedia'),

    url(r'^gallery/$', 'gallery.views.show_gallery',
        name='gallery_index'),
    url(r'^gallery/(?P<category>\w+)/$', 'gallery.views.list_albums',
        name='gallery_category_albums'),
    url(r'^gallery/(?P<category>\w+)/(?P<year>\d{4})/$', 'gallery.views.list_albums',
        name='gallery_category_albums_by_year'),
    url(r'^gallery/(?P<category>\w+)/(?P<album_slug>[-_a-zA-Z0-9]+)/$', 'gallery.views.view_album',
        name='gallery_view_album'),
    url(r'^gallery/(?P<category>\w+)/[-_a-zA-Z0-9]+/(?P<image_slug>[-_a-zA-Z0-9]+)/$', 'gallery.views.view_image',
        name='gallery_view_image'),


    url(r'^dezurstva/$', 'savjet.views.list_attendance',
        name='dezurstva'),

    # ispis crvenih za pozivnice
    url(r'^crveni/$', 'members.views.red',
        name='crveni'),
    url(r'^crveni-lista/$', 'members.views.red_list',
        name='crveni_lista'),

    url(r'^clanovi/$', 'members.views.main',
        name='members'),
    url(r'^clanovi/login/$', 'members.views.login',
        name='members_login'),
    url(r'^clanovi/logout/$', 'members.views.logout',
        name='members_logout'),
    url(r'^clanovi/svi/$', 'members.views.listAll',
        name='members_list_all'),
    url(r'^clanovi/clan/(?P<id>\d+)/$', 'members.views.member',
        name='members_show_member'),
    url(r'^clanovi/uredi/$', 'members.views.edit',
        name='members_edit'),


)

## Admin and similar
urlpatterns += patterns('',

    (r'^tinymce/', include('tinymce.urls')),

    url(r'^admin/filebrowser/', include(site.urls)),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^admin/', include(admin.site.urls)),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT}),
    )
