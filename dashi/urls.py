from django.conf.urls import *
from django.views.generic import TemplateView
from django.conf import settings
import dashi.ajax

from dajaxice.core import dajaxice_autodiscover
dajaxice_autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^dashi/', include('dashi.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    (r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
    ( r'^$', 'dashi.views.render_blocks' ),
    #( r'^$', TemplateView.as_view( template_name='dash.html') ),
)
#if settings.DEBUG:
#    urlpatterns += patterns('staticfiles.views',
#        url(r'^static/(?P<path>.*)$', 'serve'),
#    )
