from django.conf.urls import patterns, url

urlpatterns = patterns('subpages.views',
    url(r'^$', 'club',
        name='subpage_index'),
    url(r'^divisions/(?P<division>\w+)/$', 'division',
        name='subpage_division'),
    url(r'^projects/(?P<project>\w+)/$', 'project',
        name='subpage_project'),
    url(r'^multimedia/$', 'multimedia',
        name='subpage_multimedia'),
    url(r'^alumni/$', 'alumni',
        name='subpage_alumni'),
)
