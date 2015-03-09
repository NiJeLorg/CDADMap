from django.conf.urls import patterns, include, url
from django.contrib import admin
from cdadmap import urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cdad.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^', include('cdadmap.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
