from django.conf.urls import *
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from cmsplugin_blog.sitemaps import BlogSitemap

admin.autodiscover()

urlpatterns = i18n_patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^jsi18n/(?P<packages>\S+?)/$', 'django.views.i18n.javascript_catalog'),
    url(r'^', include('cms.urls')),
)


urlpatterns += patterns('',
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {
        'sitemaps': {
            'blogentries': BlogSitemap
        }
    }),
)
