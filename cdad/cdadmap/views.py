from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse

# import all cdadmap models
from cdadmap.models import *

# Create your views here.
def index(request):
    context = RequestContext(request)
    
    # get all locations and pass to template to create geojson file
    #build query
    kwargs = {}
    # show only published media
    kwargs['KeepPrivate__exact'] = 'false'
    
    #get locations
    locations = LocationPanel.objects.filter(**kwargs)
     
    context_dict = {'locations': locations}
    return render_to_response('cdadmap/index.html', context_dict, context)
    