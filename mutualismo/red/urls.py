from django.conf.urls.defaults import patterns, url

from views import index, about, contact, dashboard, offer, demand

urlpatterns = patterns('red.views',
    url(r'^$',                              index),
    url(r'^about',                          about),
    url(r'^contact',                        contact),
    url(r'^dashboard',                      dashboard),
    url(r'^offer/(?P<offer_slug>[\w-]+)',   offer),
    url(r'^demand/(?P<demand_slug>[\w-]+)', demand),
)

import settings
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
