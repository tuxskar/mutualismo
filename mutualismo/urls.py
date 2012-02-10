from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/',         include(admin.site.urls)),
    url(r'^accounts/',      include('registration.backends.default.urls')),
    url('^faq/',            include('faq.urls')),
    url(r'',                include('red.urls')),
)
