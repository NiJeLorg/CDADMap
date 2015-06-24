from django.conf.urls import patterns, include, url
from cdadmap import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^filter/$', views.filterLocations, name='filterLocations'),
    url(r'^survey/$', views.surveyPage1, name='surveyView'),
    url(r'^survey/(?P<id>\d+)/$', views.surveyPage1, name='surveyView'),
    url(r'^survey2/(?P<id>\d+)/$', views.surveyPage2, name='surveyPage2'),
    url(r'^survey3/(?P<id>\d+)/$', views.surveyPage3, name='surveyPage3'),
    url(r'^survey4/(?P<id>\d+)/$', views.surveyPage4, name='surveyPage4'),
)
