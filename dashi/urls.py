from django.conf import settings

from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView

#from dajaxice.core import dajaxice_autodiscover, dajaxice_config
#dajaxice_autodiscover()

#import dashi.ajax

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

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
    #(r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
    #url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url( r'^ajax_update_block/(?P<block_id>[0-9]+)', 'dashi.views.ajax_update_block'),
    url( r'^$', 'dashi.views.render_blocks' ),
    #( r'^$', TemplateView.as_view( template_name='dash.html') ),
)
#if settings.DEBUG:
#    urlpatterns += patterns('staticfiles.views',
#        url(r'^static/(?P<path>.*)$', 'serve'),
#    )

urlpatterns += staticfiles_urlpatterns()

