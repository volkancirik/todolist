from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^test/$', 'meccid.app.views.test'),
    url(r'^$', 'meccid.app.views.index'),
    url(r'^today/$', 'meccid.app.views.today'),
    url(r'^manage_task/$', 'meccid.app.views.manage_task'),
    url(r'^yesterday/$', 'meccid.app.views.yesterday'),
    url(r'^someday/$', 'meccid.app.views.someday'),
    url(r'^search/$', 'meccid.app.views.search'),

    # url(r'^meccid/', include('meccid.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    (r'^accounts/', include('allauth.urls'))
)
