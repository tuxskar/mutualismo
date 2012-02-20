from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/',         include(admin.site.urls)),
    url(r'^categories/',    include('categories.urls')),
    url(r'^search/',        include('haystack.urls')),
    url(r'^accounts/',      include('registration.backends.default.urls')),
    url(r'^faq/',           include('faq.urls')),
    url(r'',                include('red.urls')),
)

import settings
if settings.DEBUG:
    urlpatterns += patterns('',
        # FIXME: if we put ``static`` here it does not serve static media
        (r'^statics/(?P<path>.*)$', 'django.views.static.serve', 
            {'document_root': settings.STATIC_ROOT, 'show_indexes': True},),
    )
