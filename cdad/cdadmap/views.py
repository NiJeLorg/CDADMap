
from django.shortcuts import render
import operator
from django.db.models import TextField
from django.db.models import Q

# import all cdadmap models
from cdadmap.models import *

# Create your views here.
def index(request):
    
    # get all locations and pass to template to create geojson file
    #build query
    kwargs = {}
    # show only public locations 
    kwargs['KeepPrivate__exact'] = 'false'
    
    #get locations 
    locations = LocationPanel.objects.filter(**kwargs).order_by('Organization_Name')
        
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

    # create paths to CDO service area geojson files; SurveyPanel objects that start with {"paramName" have geoJson files assocaited with them
    staticGeoJSONs = []
    for survey in SurveyPanel.objects.filter(MapDissolve__startswith='{"paramName"'):
        survey.Organization_Name = survey.Organization_Name.replace("'", "")
        survey.Organization_Name = survey.Organization_Name.replace(" ", "")
        staticGeoJSON = 'cdadmap/geojson/' + survey.Organization_Name + '_new.json'
        staticGeoJSONs.append(staticGeoJSON);

    context_dict = {'locations': locations, "Organization_Description_Choices": Organization_Description_Choices, "Service_Area_Choices": Service_Area_Choices, "organization_structured_Choices": organization_structured_Choices, "Activities_Services_Choices": Activities_Services_Choices, "Service_Population_Choices": Service_Population_Choices, "Languages_Choices": Languages_Choices, 'staticGeoJSONs': staticGeoJSONs }
    return render(request, 'cdadmap/index.html', context_dict)
   

def filterLocations(request):
    """
      Loads the filtered locations on the map
    """
            
    # get filtered locations and pass to template to create geojson file
    # set frame for survey filters
    surveyKwargsExclude = {}
    query = Q()
    Organization_Description_query = Q()
    Service_Area_Choices_query = Q()
    organization_structured_Choices_query = Q()
    Activities_Services_Choices_query = Q()
    Service_Population_Choices_query = Q()
    Languages_Choices_query = Q()
    cdadmebership_query = Q()
    keyword_query = Q()

    #get filters
    Organization_Description_Choices = request.GET.get("Organization_Description_Choices","All")
    Service_Area_Choices = request.GET.get("Service_Area_Choices","All")
    organization_structured_Choices = request.GET.get("organization_structured_Choices","All")
    Activities_Services_Choices = request.GET.get("Activities_Services_Choices","All")
    Service_Population_Choices = request.GET.get("Service_Population_Choices","All")
    Languages_Choices = request.GET.get("Languages_Choices","All")
    cdadmebership = request.GET.get("cdadmebership","All")
    keyword = request.GET.get("keyword","All")

    #query for fields
    if(Organization_Description_Choices != ""):
        Organization_Description_ChoicesArray = Organization_Description_Choices.split('|')
        Organization_Description_query = reduce(operator.or_, (Q(Organization_Description__contains = item) for item in Organization_Description_ChoicesArray))

    if(Service_Area_Choices != ""):
        Service_Area_ChoicesArray = Service_Area_Choices.split('|')
        Service_Area_Choices_query = reduce(operator.or_, (Q(Service_Area_Description__contains = item) for item in Service_Area_ChoicesArray))


    if(organization_structured_Choices != ""):
        organization_structured_ChoicesArray = organization_structured_Choices.split('|')
        organization_structured_Choices_query = reduce(operator.or_, (Q(organization_structured__contains = item) for item in organization_structured_ChoicesArray))

    if(Activities_Services_Choices != ""):
        Activities_Services_ChoicesArray = Activities_Services_Choices.split('|')
        Activities_Services_Choices_query = reduce(operator.or_, (Q(Activities_Services__contains = item) for item in Activities_Services_ChoicesArray))

    if(Service_Population_Choices != ""):
        Service_Population_ChoicesArray = Service_Population_Choices.split('|')
        Service_Population_Choices_query = reduce(operator.or_, (Q(Service_Population__contains = item) for item in Service_Population_ChoicesArray))

    if(Languages_Choices != ""):
        Languages_ChoicesArray = Languages_Choices.split('|')
        Languages_Choices_query = reduce(operator.or_, (Q(Languages__contains = item) for item in Languages_ChoicesArray))

    if(cdadmebership != ""):
        if(cdadmebership == "Yes"):
            cdadmebership_query = Q(Languages__contains = "Currently a member")
        else:
            surveyKwargsExclude['CDAD_MemberShip__exact'] = "Currently a member"

    if(keyword != ""):
        fields = [f for f in SurveyPanel._meta.fields if isinstance(f, TextField)]
        queries = [Q(**{"%s__contains" % f.name: keyword}) for f in fields]
        for query in queries:
            keyword_query = keyword_query | query       

    # create query list from the queries that exist from above
    q_list = [Organization_Description_query, Service_Area_Choices_query, organization_structured_Choices_query, Activities_Services_Choices_query, Service_Population_Choices_query, Languages_Choices_query, cdadmebership_query, keyword_query]
    query = reduce(operator.and_, q_list)
    
    # get all survey panel objects that meet the search criteria
    surveys = SurveyPanel.objects.filter(query).exclude(**surveyKwargsExclude)
 
    #build query
    kwargs = {}
    # add returned surveys to location search
    kwargs['Organization_Name_SurveyPanel_FK__in'] = surveys

    # show only published media
    kwargs['KeepPrivate__exact'] = 'false'
 
    #get locations
    locations = LocationPanel.objects.filter(**kwargs).order_by('Organization_Name')

    # load template requested 
    template = request.GET.get("template","All")
    if (template == "locations"):
        renderTemplate = 'cdadmap/locations-geojson.html'
    else:
        renderTemplate = 'cdadmap/popup-content.html'

            
    context_dict = {'locations': locations}
    return render(request, renderTemplate, context_dict)
   