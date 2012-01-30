from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from red.views import index

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mutualismo.views.home', name='home'),
    # url(r'^mutualismo/', include('mutualismo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',      index),
)
