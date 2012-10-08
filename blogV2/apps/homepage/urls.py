from django.conf.urls import patterns, include, url

urlpatterns = patterns('blogV2.apps.homepage.views',
    url(r'^$', 'index', name="homepage_index"),
    url(r'^archive/(?P<month>\w{3})/$', 'archive', name="homepage_archiveMonth"),
    url(r'^archive/$', 'archive', name="homepage_archive"),
    url(r'^about/$', 'about', name="homepage_about"),
)
