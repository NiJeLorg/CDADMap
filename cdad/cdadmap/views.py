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
    # show only public locations 
    kwargs['KeepPrivate__exact'] = 'false'
    
    #get locations
    locations = LocationPanel.objects.filter(**kwargs)            
    
    context_dict = {'locations': locations}
    return render_to_response('cdadmap/index.html', context_dict, context)
    

def filterLocations(request):
    """
      Loads the filtered locations on the map
    """
    context = RequestContext(request)
            
    # get filtered locations and pass to template to create geojson file
    #build query
    kwargs = {}
    # show only published media
    kwargs['KeepPrivate__exact'] = 'false'
    
    #get filters
    searchOrganization_Description = request.GET.get("Organization_Description","All")
    searchOrganization_Description = request.GET.get("Organization_Description","All")
    searchOrganization_Description = request.GET.get("Organization_Description","All")
    searchOrganization_Description = request.GET.get("Organization_Description","All")
    searchOrganization_Description = request.GET.get("Organization_Description","All")
    searchOrganization_Description = request.GET.get("Organization_Description","All")
    searchOrganization_Description = request.GET.get("Organization_Description","All")
    searchOrganization_Description = request.GET.get("Organization_Description","All")
    
    #query for
    if(searchOrganization_Description != ""):
        searchOrganization_DescriptionArray = searchOrganization_Description.split(',')
        kwargs['Organization_Description__in'] = searchOrganization_DescriptionArray
    

    #get locations
    locations = LocationPanel.objects.filter(**kwargs)
            
    context_dict = {'locations': locations}
    return render_to_response('cdadmap/index.html', context_dict, context)
    