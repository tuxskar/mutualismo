from django.conf.urls.defaults import patterns, url

from views import index, about, contact, dashboard

urlpatterns = patterns('red.views',
    url(r'^$',         index),
    url(r'^about',     about),
    url(r'^contact',   contact),
    url(r'^dashboard', dashboard),
)

import settings
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
