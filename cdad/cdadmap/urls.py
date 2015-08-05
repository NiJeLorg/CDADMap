from django.conf.urls import patterns, include, url
from cdadmap import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^filter/$', views.filterLocations, name='filterLocations'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^survey/$', views.surveyPage1, name='surveyView'),
    url(r'^survey/(?P<id>\d+)/$', views.surveyPage1, name='surveyView'),
    url(r'^adminsurvey/$', views.adminSurveyPage1, name='adminSurveyView'),
    url(r'^adminsurvey/(?P<id>\d+)/$', views.adminSurveyPage1, name='adminSurveyView'),
    url(r'^survey2/(?P<id>\d+)/$', views.surveyPage2, name='surveyPage2'),
    url(r'^survey3/(?P<id>\d+)/$', views.surveyPage3, name='surveyPage3'),
    url(r'^survey4/(?P<id>\d+)/$', views.surveyPage4, name='surveyPage4'),
    url(r'^survey5/(?P<id>\d+)/$', views.surveyPage5, name='surveyPage5'),
    url(r'^survey6/(?P<id>\d+)/$', views.surveyPage6, name='surveyPage6'),
    url(r'^survey7/(?P<id>\d+)/$', views.surveyPage7, name='surveyPage7'),
    url(r'^getjsonformap/(?P<id>\d+)/$', views.getJSONforMap, name='getJSONforMap'),
    url(r'^survey7save/(?P<id>\d+)/$', views.surveyPage7save, name='surveyPage7save'),
    url(r'^survey8/(?P<id>\d+)/$', views.surveyPage8, name='surveyPage8'),
    url(r'^survey9/(?P<id>\d+)/$', views.surveyPage9, name='surveyPage9'),
    url(r'^survey10/(?P<id>\d+)/$', views.surveyPage10, name='surveyPage10'),
    url(r'^survey11/(?P<id>\d+)/$', views.surveyPage11, name='surveyPage11'),
    url(r'^survey12/(?P<id>\d+)/$', views.surveyPage12, name='surveyPage12'),
    url(r'^survey13/(?P<id>\d+)/$', views.surveyPage13, name='surveyPage13'),
    url(r'^survey14/(?P<id>\d+)/$', views.surveyPage14, name='surveyPage14'),
    url(r'^surveyfinish/(?P<id>\d+)/$', views.surveyfinish, name='surveyfinish'),
    url(r'^verifysurvey/(?P<id>\d+)/$', views.verifysurvey, name='verifysurvey'),
    url(r'^removesurvey/(?P<id>\d+)/$', views.removesurvey, name='removesurvey'),
    url(r'^adminregister/$', views.adminRegister, name='adminRegister'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
