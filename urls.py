from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # feeds
    #(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),


    ### PROGRAM

    # news - homepage
    url(r'^$', 'news.views.active', name='root'),
    url(r'^arhiva/vijesti/', 'news.views.archive', name='news-archive'), 
    url(r'^vijest/(?P<slug>[-a-zA-Z0-9]+)/$', 'news.views.by_slug', name='news-slug'), 
                       
    # events
    url(r'^arhiva/dogadaji/(?P<year>\d{4})/', 'events.views.archive', name='events-archive-year'), 
    url(r'^arhiva/dogadaji/', 'events.views.archive', name='events-archive'), 
    url(r'^dogadaj/(?P<slug>[-a-zA-Z0-9]+)/$', 'events.views.by_slug', name='event-slug'), 
    url(r'^kalendar/$', 'events.views.calendar', name="calendar"),
    url(r'^dogadaji/(?P<date>[-0-9]+)/$', 'events.views.by_date', name='events-date'), 
    
    #url(r'^events/id/(?P<event_id>\d+)/$', 'events.views.events_by_id', name='events-id'), 
    #url('^events/rdf/$', 'events.views.events_rdf', name="events-rdf"),

    # newsletter
    url(r'^newsletter/$', 'events.views.newsletter', name='newsletter'), 
    url(r'^subscribe/$', 'newsletter.views.subscribe',name='subscribe'),
    #url(r'^unsubscribe/$', 'newsletter.views.unsubscribe',name='unsubscribe'),
    #url(r'^listsubscriptions/$','newsletter.views.list_subscriptions',name='listsubscriptions'),
 
    # search
    url(r'^trazi/$', 'search.views.search', name='search'), 


    ###  CLUB

    #url(r'^klub/clanovi/$', 'members.views.list', name='members'),

    url(r'^klub/sekcije/(?P<slug>[-a-zA-Z0-9]+)/$', 'subpages.views.by_slug', name='subpage-slug'),
    url(r'^klub/alumni/$', 'subpages.views.by_slug', {'slug': 'alumni',}, name='alumni'),
    url(r'^klub/$', 'subpages.views.by_slug', name='club'),
    #url(r'^dezurstva/$','subpages.views.by_slug', name='dezurstva'),


    ###  MULTIMEDIA                       

    url(r'^multimedia/$', 'subpages.views.multimedia', name='multimedia'),

    #### Jebena dezurstva da me prestanu ispitivat stalno svi
    url(r'^dezurstva/$', 'savjet.views.list_attendance', name='dezurstva')


)

urlpatterns += patterns('',

    ### ADMIN

    (r'^tagging_autocomplete/', include('tagging_autocomplete.urls')),
                       
    (r'^admin/filebrowser/', include('filebrowser.urls')),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^admin/', include(admin.site.urls)),
)

