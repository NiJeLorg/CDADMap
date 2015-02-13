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
    
    #get locations but exclude NULL or empty Lat Lon values
    locations = LocationPanel.objects.filter(**kwargs).exclude(Lat__isnull=True).exclude(Lat__exact='').exclude(Lon__isnull=True).exclude(Lon__exact='')

    # now get a set of locations where no Lat/Lon exists
    #kwargs['Lat__in'] = ['', 'NULL']
    #kwargs['Lon__in'] = ['', 'NULL']
    kwargs['Lat__exact'] = '' 
    kwargs['Lon__exact'] = '' 
    locationsWithoutLatLon = LocationPanel.objects.filter(**kwargs)
        
    # get lists of options for filters
    Organization_Description_Choices_Array = []
    Organization_Description_Choices_List = SurveyPanel.objects.values_list('Organization_Description', flat=True)
    for choice in Organization_Description_Choices_List:
        choice_string = str(choice)
        split_choices = choice_string.split(', ');
        Organization_Description_Choices_Array.extend(split_choices)   
        
    Organization_Description_Choices = list(set(Organization_Description_Choices_Array))
    Organization_Description_Choices.sort()


    Service_Area_Choices_Array = []
    Service_Area_Choices_List = SurveyPanel.objects.values_list('Service_Area_Description', flat=True)    
    for choice in Service_Area_Choices_List:
        choice_string = str(choice)
        split_choices = choice_string.split(',');
        Service_Area_Choices_Array.extend(split_choices)   

    Service_Area_Choices = list(set(Service_Area_Choices_Array))
    Service_Area_Choices.sort()


    organization_structured_Choices_Array = []
    organization_structured_Choices_List = SurveyPanel.objects.values_list('organization_structured', flat=True)
    for choice in organization_structured_Choices_List:
        choice_string = str(choice)
        choice_string_replace = choice_string.replace(', ', '| ')
        split_choices = choice_string_replace.split(',')
        organization_structured_Choices_Array.extend(s.replace('| ', ', ') for s in split_choices)   

    organization_structured_Choices = list(set(organization_structured_Choices_Array))        
    organization_structured_Choices.sort()

    Activities_Services_Choices_Array = []
    Activities_Services_Choices_List = SurveyPanel.objects.values_list('Activities_Services', flat=True)    
    for choice in Activities_Services_Choices_List:
        choice_string = str(choice)
        choice_string_replace = choice_string.replace(', ', '| ')
        split_choices = choice_string_replace.split(',')
        Activities_Services_Choices_Array.extend(s.replace('| ', ', ') for s in split_choices)   

    Activities_Services_Choices = list(set(Activities_Services_Choices_Array))        
    Activities_Services_Choices.sort()

    Service_Population_Choices_Array = []
    Service_Population_Choices_List = SurveyPanel.objects.values_list('Service_Population', flat=True)    
    for choice in Service_Population_Choices_List:
        choice_string = str(choice)
        choice_string_replace = choice_string.replace(', ', '| ')
        split_choices = choice_string_replace.split(',')
        Service_Population_Choices_Array.extend(s.replace('| ', ', ') for s in split_choices)   

    Service_Population_Choices = list(set(Service_Population_Choices_Array))        
    Service_Population_Choices.sort()

    Languages_Choices_Array = []
    Languages_Choices_List = SurveyPanel.objects.values_list('Languages', flat=True)    
    for choice in Languages_Choices_List:
        choice_string = str(choice)
        choice_string_replace = choice_string.replace(', ', '| ')
        split_choices = choice_string_replace.split(',')
        Languages_Choices_Array.extend(s.replace('| ', ', ') for s in split_choices)   

    Languages_Choices = list(set(Languages_Choices_Array))        
    Languages_Choices.sort()




    context_dict = {'locations': locations, 'locationsWithoutLatLon': locationsWithoutLatLon, "Organization_Description_Choices": Organization_Description_Choices, "Service_Area_Choices": Service_Area_Choices, "organization_structured_Choices": organization_structured_Choices, "Activities_Services_Choices": Activities_Services_Choices, "Service_Population_Choices": Service_Population_Choices, "Languages_Choices": Languages_Choices }
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
    