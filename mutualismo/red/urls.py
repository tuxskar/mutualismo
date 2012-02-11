from django.conf.urls.defaults import patterns, url

from views import *

urlpatterns = patterns('red.views',
    url(r'^$',                                     index),
    url(r'^about',                                 about),
    url(r'^contact',                               contact),
    url(r'^dashboard',                             dashboard),
    url(r'^offer/(?P<offer_slug>[\w-]+)',          offer),
    url(r'^demand/(?P<demand_slug>[\w-]+)',        demand),
    url(r'^create/demand',                         create_demand),
    url(r'^create/service',                        create_service),
    url(r'^delete/offer/(?P<offer_slug>[\w-]+)',   delete_offer),
    url(r'^delete/demand/(?P<demand_slug>[\w-]+)', delete_demand),
)
