from django.conf.urls.defaults import patterns, url
from django.contrib.auth.views import login, logout

from views import index, about, contact

urlpatterns = patterns('red.views',
    url(r'^$',        index),
    url(r'^about',    about),
    url(r'^contact',  contact),
    url(r'^login',  login),
    #url(r'^logout/$', logout, {'next_page': ''}),
)

import settings
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
