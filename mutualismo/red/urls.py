from django.conf.urls.defaults import patterns, url

from views import *

urlpatterns = patterns('red.views',
    url(r'^$',                                     index,),
    url(r'^about',                                 about, name='about'),
    url(r'^contact',                               contact, name='contact'),
    url(r'^dashboard',                             dashboard, name='dashboard'),
    url(r'^offer/(?P<offer_slug>[\w-]+)',          offer, name='offer'),
    url(r'^demand/(?P<demand_slug>[\w-]+)',        demand, name='demand'),
    url(r'^create/demand',                         create_demand, name='new_demand'),
    url(r'^delete/offer/(?P<offer_slug>[\w-]+)',   delete_offer, name='delete_offer'),
    url(r'^delete/demand/(?P<demand_slug>[\w-]+)', delete_demand, name='delete_demand'),
)

import settings
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': setings.STATIC_ROOT}),
    )
