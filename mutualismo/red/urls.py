from django.conf.urls.defaults import patterns, include, url

from views import index, about, contact

urlpatterns = patterns('red.views',
    url(r'^$',       index),
    url(r'^about',   about),
    url(r'^contact', contact),
)
