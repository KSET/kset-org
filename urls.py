from django.conf.urls.defaults import *
from feed import RssProgramFeed, AtomProgramFeed

from django.contrib import admin

from filebrowser.sites import site

admin.autodiscover()

feeds = {
    'rss': RssProgramFeed,
    'atom': AtomProgramFeed,
    }

urlpatterns = patterns('',

    # feeds
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    
    ### PROGRAM

    # news - homepage
    url(r'^$', 'news.views.active', name='root'),
    url(r'^arhiva/vijesti/', 'news.views.archive', name='news-archive'), 
    url(r'^vijest/(?P<slug>[-a-zA-Z0-9]+)/$', 'news.views.by_slug', name='news-slug'), 
    
    ## jobfair print cvs to pdf
    #url(r'^jobfair/$', 'zivpdf.views.get_cvs', name='jobfair-cvs'),


                   
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


    ###  MULTIMEDIA                       

    url(r'^multimedia/$', 'subpages.views.multimedia', name='multimedia'),

    url(r'^gallery/$', 'gallery.views.show_gallery'),
    url(r'^gallery/(?P<cat>live)/$', 'gallery.views.list_albums'),
    url(r'^gallery/(?P<cat>foto)/$', 'gallery.views.list_albums'),
    url(r'^gallery/live/(?P<album_slug>[-_a-zA-Z0-9]+)/$', 'gallery.views.view_album'),
    url(r'^gallery/foto/(?P<album_slug>[-_a-zA-Z0-9]+)/$', 'gallery.views.view_album'),
    url(r'^gallery/(?P<cat>live)/albumi/(?P<year>\d{4})/$', 'gallery.views.list_albums'),
    url(r'^gallery/(?P<cat>foto)/albumi/(?P<year>\d{4})/$', 'gallery.views.list_albums'),
    url(r'^gallery/live/[-_a-zA-Z0-9]+/(?P<image_slug>[-_a-zA-Z0-9]+)/$', 'gallery.views.view_image' ),
    url(r'^gallery/foto/[-_a-zA-Z0-9]+/(?P<image_slug>[-_a-zA-Z0-9]+)/$', 'gallery.views.view_image' ),


    #### dezurstva
    url(r'^dezurstva/$', 'savjet.views.list_attendance', name='dezurstva'),

    # ispis crvenih za pozivnice
    url(r'^crveni/$', 'members.views.red', name='crveni'),
    url(r'^crveni-lista/$', 'members.views.red_list', name='crveni-lista'),

	###	 MEMEBERS
	
	# check!!
	
	url(r'^clanovi/$', 'members.views.main', name='members'),
	url(r'^clanovi/login/$', 'members.views.login', name='members-login'),
	url(r'^clanovi/logout/$', 'members.views.logout', name='members-logout'),
	url(r'^clanovi/svi/$', 'members.views.listAll', name='members-list-all'),
	url(r'^clanovi/clan/([0-9]+)/$', 'members.views.member', name='members-show-member'),
	url(r'^clanovi/uredi/$', 'members.views.edit', name='members-edit'),
	#url(r'^clanovi/uredi/submit/$', 'members.views.submit', name='members-edit-submit'),


)

urlpatterns += patterns('',

    ### ADMIN

    (r'^tagging_autocomplete/', include('tagging_autocomplete.urls')),
    (r'^tinymce/', include('tinymce.urls')),

    url(r'^admin/filebrowser/', include(site.urls)),                       
    (r'^grappelli/', include('grappelli.urls')),
    (r'^admin/', include(admin.site.urls)),
)

