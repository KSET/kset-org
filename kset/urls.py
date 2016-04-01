from django.conf.urls import url, patterns, include
from django.contrib import admin
from django.conf import settings

from feed import RssProgramFeed, AtomProgramFeed
from filebrowser.sites import site

import members.urls
import gallery.urls
import subpages.urls

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^i18n/', include('django.conf.urls.i18n')),

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

    url(r'^dezurstva/$', 'savjet.views.list_attendance',
        name='dezurstva'),

    url(r'^gallery/', include(gallery.urls)),
    url(r'^members/', include(members.urls)),
    url(r'^club/', include(subpages.urls)),

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
