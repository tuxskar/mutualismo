from django.conf.urls.defaults import patterns, url

from views import *

urlpatterns = patterns('red.views',
    url(r'^$',                                     index, name='index'),
    url(r'^about',                                 about, name='about'),
    url(r'^contact',                               contact, name='contact'),
    url(r'^dashboard',                             dashboard, name='dashboard'),
    url(r'^offer/(?P<offer_slug>[\w-]+)',          offer),
    url(r'^demand/(?P<demand_slug>[\w-]+)',        demand),
    url(r'^edit/demand/(?P<demand_slug>[\w-]+)',   edit_demand),
    url(r'^edit/service/(?P<service_slug>[\w-]+)', edit_service),
    url(r'^edit/gift/(?P<gift_slug>[\w-]+)',       edit_gift),
    url(r'^edit/loan/(?P<loan_slug>[\w-]+)',       edit_loan),
    url(r'^create/demand',                         create_demand),
    url(r'^create/service',                        create_service),
    url(r'^create/gift',                           create_gift),
    url(r'^create/loan',                           create_loan),
    url(r'^delete/offer/(?P<offer_slug>[\w-]+)',   delete_offer),
    url(r'^delete/demand/(?P<demand_slug>[\w-]+)', delete_demand),
)
