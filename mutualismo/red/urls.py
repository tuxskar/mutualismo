from django.conf.urls.defaults import patterns, url

from views import *

urlpatterns = patterns('red.views',
    url(r'^$'                                    , index         , name='index'),
    url(r'^about'                                , about         , name='about'),
    url(r'^contact'                              , contact       , name='contact'),
    url(r'^dashboard'                            , dashboard     , name='dashboard'),
    url(r'^offer/(?P<offer_slug>[\w-]+)'         , offer),
    url(r'^demand/(?P<demand_slug>[\w-]+)'       , demand),
    url(r'^create/demand'                        , create_demand , name='create_demand'),
    url(r'^create/service'                       , create_service, name='create_service'),
    url(r'^create/gift'                          , create_gift   , name='create_gift'),
    url(r'^create/loan'                          , create_loan   , name='create_loan'),
    url(r'^delete/offer/(?P<offer_slug>[\w-]+)'  , delete_offer  , name='delete_offer'),
    url(r'^delete/demand/(?P<demand_slug>[\w-]+)', delete_demand , name='delete_demand'),
)
