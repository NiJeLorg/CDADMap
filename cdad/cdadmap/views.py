
import sys,os,urllib,urllib2,json,re
from django.shortcuts import render
import operator
from django.db.models import TextField
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.forms.models import modelformset_factory

# import all cdadmap models and forms
from cdadmap.forms import *
from cdadmap.models import *

# login required decorator
from django.contrib.auth.decorators import login_required

#CSRF decorator
from django.views.decorators.csrf import ensure_csrf_cookie

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
	elif (template == "popup"):
		renderTemplate = 'cdadmap/popup-content.html'
	else:
		renderTemplate = 'cdadmap/org-modal.html'

			
	context_dict = {'locations': locations}
	return render(request, renderTemplate, context_dict)


# survey views
@login_required
def surveyPage1(request, id=None):

	if id:
		surveyObject = SurveyPanel.objects.get(id=id)
	else:
		surveyObject = SurveyPanel()

	# A HTTP POST?
	if request.method == 'POST':
		form = Page1Form(request.POST, instance=surveyObject)

		# Have we been provided with a valid form?
		if form.is_valid():
			# Save the new data to the database.
			f = form.save(commit=False)
			# add current user
			f.user = request.user
			# mark as draft
			f.verified = False
			f.save()
			lookupObject = SurveyPanel.objects.get(Organization_Name=f.Organization_Name)
			return HttpResponseRedirect(reverse('surveyPage2', args=(lookupObject.pk,)))
		else:
			# The supplied form contained errors - just print them to the terminal.
			print form.errors
	else:
		# If the request was not a POST, display the form to enter details.
		form = Page1Form(instance=surveyObject)

	# Bad form (or form details), no form supplied...
	# Render the form with error messages (if any).
	return render(request, 'cdadsurvey/surveyPage1.html', {'form': form})


@login_required
def surveyPage2(request, id=None, passed=False):

	surveyObject = SurveyPanel.objects.get(id=id)

	# A HTTP POST?
	if request.method == 'POST' and passed == False:
		form = Page2Form(request.POST, request.FILES, instance=surveyObject)

		# Have we been provided with a valid form?
		if form.is_valid():
			# Save the new data to the database.
			form.save(commit=True)

			return HttpResponseRedirect(reverse('surveyPage3', args=(id,)))
		else:
			# The supplied form contained errors - just print them to the terminal.
			print form.errors
	else:
		# If the request was not a POST, display the form to enter details.
		form = Page2Form(instance=surveyObject)

	# Bad form (or form details), no form supplied...
	# Render the form with error messages (if any).
	return render(request, 'cdadsurvey/surveyPage2.html', {'form': form, 'id':id})


@login_required
def surveyPage3(request, id=None, passed=False):

	surveyObject = SurveyPanel.objects.get(id=id)

	# A HTTP POST?
	if request.method == 'POST' and passed == False:
		form = Page3Form(request.POST, request.FILES, instance=surveyObject)

		# Have we been provided with a valid form?
		if form.is_valid():
			# Save the new data to the database.
			form.save(commit=True)

			return HttpResponseRedirect(reverse('surveyPage4', args=(id,)))
		else:
			# The supplied form contained errors - just print them to the terminal.
			print form.errors
	else:
		# If the request was not a POST, display the form to enter details.
		form = Page3Form(instance=surveyObject)

	# Bad form (or form details), no form supplied...
	# Render the form with error messages (if any).
	return render(request, 'cdadsurvey/surveyPage3.html', {'form': form, 'id':id})


@login_required
def surveyPage4(request, id=None, passed=False):

	surveyObject = SurveyPanel.objects.get(id=id)
	contactObjects = ContactPanel.objects.filter(Organization_Name=surveyObject.Organization_Name)
	ContactFormset = modelformset_factory(ContactPanel, form=Page4Form, extra=10, can_delete=True, validate_min=True, min_num=1)

	# A HTTP POST?
	if request.method == 'POST' and passed == False:
		formset = ContactFormset(request.POST, queryset=contactObjects)

		# Have we been provided with a valid form?
		if formset.is_valid():
			# Save the new data to the database.
			instances = formset.save(commit=False)
			# delete any objects if checked for deletion
			for obj in formset.deleted_objects:
				obj.delete()

			for instance in instances:
				instance.Organization_Name = surveyObject.Organization_Name
				instance.save()

			return HttpResponseRedirect(reverse('surveyPage5', args=(id,)))

		else:
			# The supplied form contained errors - just print them to the terminal.
			print formset.errors

	else:
		# If the request was not a POST, display the form to enter details.
		formset = ContactFormset(queryset=contactObjects)

	# Bad form (or form details), no form supplied...
	# Render the form with error messages (if any).
	return render(request, 'cdadsurvey/surveyPage4.html', {'formset': formset, 'id':id})
   

@login_required
def surveyPage5(request, id=None, passed=False):

	# get base URL and params for geocoding
	base_url = "http://maps.googleapis.com/maps/api/geocode/json?"

	surveyObject = SurveyPanel.objects.get(id=id)
	locationObjects = LocationPanel.objects.filter(Organization_Name=surveyObject.Organization_Name)
	LocationFormset = modelformset_factory(LocationPanel, form=Page5Form, extra=10, can_delete=True, validate_min=True, min_num=1)

	# A HTTP POST?
	if request.method == 'POST' and passed == False:
		formset = LocationFormset(request.POST, queryset=locationObjects)

		# Have we been provided with a valid form?
		if formset.is_valid():
			# Save the new data to the database.
			instances = formset.save(commit=False)
			# delete any objects if checked for deletion
			for obj in formset.deleted_objects:
				obj.delete()
				
			for instance in instances:
				instance.Organization_Name = surveyObject.Organization_Name
				# geocoding
				if bool(instance.MailingAddress) == False:
					if bool(instance.City) is True:
						fullAddress = instance.Address + ' ' + instance.City + ', ' + instance.State
						params = { 'address' : fullAddress, 'sensor' : "false" }                    
					else:
						fullAddress = instance.Address + ', ' + instance.State
						params = { 'address' : fullAddress, 'sensor' : "false" }

					# fully form url    
					request_url = base_url + urllib.urlencode(params);
					
					#send request to google and decode the returned JSON into a string
					response = json.loads(urllib2.urlopen(request_url).read(1000000))
				
					# pull out and save the lat & lons            
					instance.Lat = response['results'][0]['geometry']['location']['lat']	    	
					instance.Lon = response['results'][0]['geometry']['location']['lng']                   
				else:
					instance.Lat = 0
					instance.Lon = 0

				instance.Organization_Name_SurveyPanel_FK = surveyObject

				instance.save()

			return HttpResponseRedirect(reverse('surveyPage6', args=(id,)))
		else:
			# The supplied form contained errors - just print them to the terminal.
			print formset.errors
	else:
		# If the request was not a POST, display the form to enter details.
		formset = LocationFormset(queryset=locationObjects)

	# Bad form (or form details), no form supplied...
	# Render the form with error messages (if any).
	return render(request, 'cdadsurvey/surveyPage5.html', {'formset': formset, 'id':id})


@login_required
def surveyPage6(request, id=None, passed=False):

	surveyObject = SurveyPanel.objects.get(id=id)

	# A HTTP POST?
	if request.method == 'POST' and passed == False:
		form = Page6Form(request.POST, instance=surveyObject)

		# Have we been provided with a valid form?
		if form.is_valid():
			# Save the new data to the database.
			form.save(commit=True)

			return HttpResponseRedirect(reverse('surveyPage7', args=(id,)))
		else:
			# The supplied form contained errors - just print them to the terminal.
			print form.errors
	else:
		# If the request was not a POST, display the form to enter details.
		form = Page6Form(instance=surveyObject)

	# Bad form (or form details), no form supplied...
	# Render the form with error messages (if any).
	return render(request, 'cdadsurvey/surveyPage6.html', {'form': form, 'id':id})


@login_required
@ensure_csrf_cookie
def surveyPage7(request, id=None, passed=False):

	surveyObject = SurveyPanel.objects.get(id=id)

	return render(request, 'cdadsurvey/surveyPage7.html', {'surveyObject': surveyObject, 'id':id})


def getJSONforMap(request, id=None, passed=False):

	surveyObject = SurveyPanel.objects.get(id=id)

	return JsonResponse(surveyObject.MapDissolve, safe=False)


def surveyPage7save(request, id=None):

	# A HTTP POST?
	if request.method == 'POST':
		# update record with geojson
		SurveyPanel.objects.filter(id=id).update(MapDissolve=request.POST['geojson'])
	else:
		empty = {}

	# Bad form (or form details), no form supplied...
	return JsonResponse(request.POST)


@login_required
def surveyPage8(request, id=None, passed=False):

	surveyObject = SurveyPanel.objects.get(id=id)

	# A HTTP POST?
	if request.method == 'POST' and passed == False:
		form = Page8Form(request.POST, instance=surveyObject)

		# Have we been provided with a valid form?
		if form.is_valid():
			# Save the new data to the database.
			form.save(commit=True)

			return HttpResponseRedirect(reverse('surveyPage9', args=(id,)))
		else:
			# The supplied form contained errors - just print them to the terminal.
			print form.errors
	else:
		# If the request was not a POST, display the form to enter details.
		form = Page8Form(instance=surveyObject)

	# Bad form (or form details), no form supplied...
	# Render the form with error messages (if any).
	return render(request, 'cdadsurvey/surveyPage8.html', {'form': form, 'id':id})
   

@login_required
def surveyPage9(request, id=None, passed=False):

	surveyObject = SurveyPanel.objects.get(id=id)

	# A HTTP POST?
	if request.method == 'POST' and passed == False:
		form = Page9Form(request.POST, instance=surveyObject)

		# Have we been provided with a valid form?
		if form.is_valid():
			# Save the new data to the database.
			form.save(commit=True)

			return HttpResponseRedirect(reverse('surveyPage10', args=(id,)))
		else:
			# The supplied form contained errors - just print them to the terminal.
			print form.errors
	else:
		# If the request was not a POST, display the form to enter details.
		form = Page9Form(instance=surveyObject)

	# Bad form (or form details), no form supplied...
	# Render the form with error messages (if any).
	return render(request, 'cdadsurvey/surveyPage9.html', {'form': form, 'id':id})
   

@login_required
def surveyPage10(request, id=None, passed=False):

	surveyObject = SurveyPanel.objects.get(id=id)
	# creating a Python list from string 
	surveyObject.Languages_Other = surveyObject.Languages_Other.strip('[]').replace("u'","").replace("'","").split(', ')
	surveyObject.Languages_Other = ", ".join(str(lang) for lang in surveyObject.Languages_Other)

	# A HTTP POST?
	if request.method == 'POST' and passed == False:
		form = Page10Form(request.POST, instance=surveyObject)

		# Have we been provided with a valid form?
		if form.is_valid():
			# Save the new data to the database.
			f = form.save(commit=False)
			# create python list from languages in "not a word" seperated values
			f.Languages_Other = re.split( '\W+' , request.POST['Languages_Other'] )
			f.save()

			return HttpResponseRedirect(reverse('surveyPage11', args=(id,)))
		else:
			# The supplied form contained errors - just print them to the terminal.
			print form.errors
	else:
		# If the request was not a POST, display the form to enter details.
		form = Page10Form(instance=surveyObject)

	# Bad form (or form details), no form supplied...
	# Render the form with error messages (if any).
	return render(request, 'cdadsurvey/surveyPage10.html', {'form': form, 'id':id})


@login_required
def surveyPage11(request, id=None, passed=False):

	surveyObject = SurveyPanel.objects.get(id=id)
	meetingObjects = MeetingPanel.objects.filter(Organization_Name=surveyObject.Organization_Name)
	MeetingFormset = modelformset_factory(MeetingPanel, form=Page11Form, extra=4, can_delete=True)

	# A HTTP POST?
	if request.method == 'POST' and passed == False:
		formset = MeetingFormset(request.POST, queryset=meetingObjects)

		# Have we been provided with a valid form?
		if formset.is_valid():
			# Save the new data to the database.
			instances = formset.save(commit=False)
			# delete any objects if checked for deletion
			for obj in formset.deleted_objects:
				obj.delete()	

			for instance in instances:
				instance.Organization_Name = surveyObject.Organization_Name
				instance.save()

			return HttpResponseRedirect(reverse('surveyPage12', args=(id,)))

		else:
			# The supplied form contained errors - just print them to the terminal.
			print formset.errors

	else:
		# If the request was not a POST, display the form to enter details.
		formset = MeetingFormset(queryset=meetingObjects)

	# Bad form (or form details), no form supplied...
	# Render the form with error messages (if any).
	return render(request, 'cdadsurvey/surveyPage11.html', {'formset': formset, 'id':id})


@login_required
def surveyPage12(request, id=None, passed=False):

	surveyObject = SurveyPanel.objects.get(id=id)

	# A HTTP POST?
	if request.method == 'POST' and passed == False:
		form = Page12Form(request.POST, instance=surveyObject)

		# Have we been provided with a valid form?
		if form.is_valid():
			# Save the new data to the database.
			form.save(commit=True)

			return HttpResponseRedirect(reverse('surveyPage13', args=(id,)))
		else:
			# The supplied form contained errors - just print them to the terminal.
			print form.errors
	else:
		# If the request was not a POST, display the form to enter details.
		form = Page12Form(instance=surveyObject)

	# Bad form (or form details), no form supplied...
	# Render the form with error messages (if any).
	return render(request, 'cdadsurvey/surveyPage12.html', {'form': form, 'id':id})


@login_required
def surveyPage13(request, id=None, passed=False):

	surveyObject = SurveyPanel.objects.get(id=id)
	PartnerFormset = modelformset_factory(Partners, form=AddParner, extra=5)

	# A HTTP POST?
	if request.method == 'POST' and passed == False:
		form = Page13Form(request.POST, instance=surveyObject)
		formset = PartnerFormset(request.POST, queryset=Partners.objects.none())

		# Have we been provided with a valid form?
		if form.is_valid() and formset.is_valid():
			# Save the new data to the database.
			form.save(commit=True)
			formset.save(commit=True)

			return HttpResponseRedirect(reverse('surveyPage14', args=(id,)))
		else:
			# The supplied form contained errors - just print them to the terminal.
			print form.errors
	else:
		# If the request was not a POST, display the form to enter details.
		form = Page13Form(instance=surveyObject)
		formset = PartnerFormset(queryset=Partners.objects.none())

	# Bad form (or form details), no form supplied...
	# Render the form with error messages (if any).
	return render(request, 'cdadsurvey/surveyPage13.html', {'form': form, 'formset':formset, 'id':id})

@login_required
def surveyPage14(request, id=None, passed=False):

	surveyObject = SurveyPanel.objects.get(id=id)

	# A HTTP POST?
	if request.method == 'POST' and passed == False:
		form = Page14Form(request.POST, instance=surveyObject)

		# Have we been provided with a valid form?
		if form.is_valid():
			# Save the new data to the database.
			form.save(commit=True)

			return HttpResponseRedirect(reverse('surveyfinish', args=(id,)))
		else:
			# The supplied form contained errors - just print them to the terminal.
			print form.errors
	else:
		# If the request was not a POST, display the form to enter details.
		form = Page14Form(instance=surveyObject)

	# Bad form (or form details), no form supplied...
	# Render the form with error messages (if any).
	return render(request, 'cdadsurvey/surveyPage14.html', {'form': form, 'id':id})


@login_required
def surveyfinish(request, id=None):

	return render(request, 'cdadsurvey/surveyfinish.html', {'id':id})


