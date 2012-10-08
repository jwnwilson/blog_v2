from django.conf.urls import patterns, include, url
from blogV2 import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^', include('blogV2.apps.homepage.urls') ),
	(r'^', include('blogV2.apps.accounts.urls') ),
    # Examples:
    # url(r'^$', 'blogV2.views.home', name='home'),
    # url(r'^blogV2/', include('blogV2.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
	urlpatterns += patterns('',
		(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
	)
