from django.conf.urls import patterns, include, url
from django.contrib import admin
from cdadmap import urls

urlpatterns = patterns('',    
    url(r'^', include('cdadmap.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^select2/', include('django_select2.urls')),
)
