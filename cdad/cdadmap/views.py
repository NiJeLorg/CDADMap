
import sys,os,urllib,urllib2,json,re,zipfile,csv
from django.shortcuts import render
import operator
from django.db.models import TextField
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.forms.models import modelformset_factory
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail

# path to media root for adding a zip archive
from django.core.files import File
from django.conf import settings
MEDIA_ROOT = settings.MEDIA_ROOT
GEOCODER_API_KEY = settings.GEOCODER_API_KEY

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

	#get locations only from verified surveys
	kwargs['Organization_Name_SurveyPanel_FK__verified__exact'] = True

	#get locations 
	locations = LocationPanel.objects.filter(**kwargs).order_by('Organization_Name')

	# create Activity list and strip out address if address is private
	for location in locations:
		location.Activity = location.Activity.strip('[]').replace("u'","").replace("'","").split(', ')
		if location.KeepPrivate:
			location.Address = ''

	# figure out which Surveys have geojsons
	surveys_with_maps_ids = []
	for location in locations:
		survey = SurveyPanel.objects.get(Organization_Name=location.Organization_Name_SurveyPanel_FK)
		if survey.MapDissolve:
			surveys_with_maps_ids.append(survey.id)

	surveys_with_maps_ids = set(surveys_with_maps_ids)
	surveys_with_maps_ids = list(surveys_with_maps_ids)
		
	context_dict = {'locations': locations, "Organization_Description_Choices": ORG_DESCRIPTION_CHOICES, "Service_Area_Choices": SERVICE_AREA_CHOICES, "organization_structured_Choices": STRUCTURE_CHOICES, "Activities_Services_Choices": ACTIVITY_SERVICES_CHOICES, "Service_Population_Choices": POPULATION_CHOICES, "Languages_Choices": LANGUAGE_CHOICES, 'surveys_with_maps_ids':surveys_with_maps_ids, 'Council_District_Choices':COUNCIL_DISTRICT_CHOICES, 'GEOCODER_API_KEY':GEOCODER_API_KEY}
	return render(request, 'cdadmap/index.html', context_dict)


def getLocationDataForCDOBCLAYER(request):

	response = {}

	Organization_Name = request.GET.get("Organization_Name","")
	
	#get locations 
	location = LocationPanel.objects.get(Organization_Name__exact=Organization_Name)
	survey = SurveyPanel.objects.get(Organization_Name__exact=Organization_Name)

	# create Activity list
	location.Activity = location.Activity.strip('[]').replace("u'","").replace("'","")
	if location.KeepPrivate:
		location.Address = ''

	# create Activities Services
	survey.Activities_Services = survey.Activities_Services.strip('[]').replace("u'","").replace("'","")

	survey.Organization_Description = survey.Organization_Description.strip('[]').replace("u'","").replace("'","")

	response['idlocation'] = location.idlocation
	response['Organization_Name'] = location.Organization_Name
	response['Organizaton_Acronym'] = survey.Organizaton_Acronym
	response['Organization_Logo_Image'] = '/media/' + str(survey.Organization_Logo_Image)
	response['Address'] = location.Address
	response['Address2'] = location.Address2
	response['City'] = location.City
	response['ZipCode'] = location.ZipCode
	response['State'] = location.State
	response['MailingAddress'] = location.MailingAddress
	response['Activity'] = location.Activity
	response['Activity_Other'] = location.Activity_Other
	response['Organization_Description'] = survey.Organization_Description
	response['Organization_Description_Other'] = survey.Organization_Description_Other
	response['Activities_Services'] = survey.Activities_Services
	response['Email'] = survey.Social_Email
	if survey.Social_Phone_KeepPrivate:
		response['Phone'] = ''
	else:
		response['Phone'] = survey.Social_Phone
	response['Social_website'] = survey.Social_website
	response['Social_facebook'] = survey.Social_facebook
	response['Social_Twitter'] = survey.Social_Twitter
	response['youtube'] = survey.youtube
	response['instagram'] = survey.instagram
	response['nextdoor'] = survey.nextdoor

	return JsonResponse(response)
   

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
	Languages_Other_query = Q()
	cdadmebership_query = Q()
	Council_District_Choices_query = Q()
	keyword_query = Q()
	verified_query = Q(verified__exact = True)

	#get filters
	Organization_Description_Choices = request.GET.get("Organization_Description_Choices","")
	Service_Area_Choices = request.GET.get("Service_Area_Choices","")
	organization_structured_Choices = request.GET.get("organization_structured_Choices","")
	Activities_Services_Choices = request.GET.get("Activities_Services_Choices","")
	Service_Population_Choices = request.GET.get("Service_Population_Choices","")
	Languages_Choices = request.GET.get("Languages_Choices","")
	Languages_Other = request.GET.get("Languages_Other","")
	cdadmebership = request.GET.get("cdadmebership","")
	Council_District_Choices = request.GET.get("Council_District_Choices","")
	keyword = request.GET.get("keyword","")

	#query for fields
	if(Organization_Description_Choices != ""):
		Organization_Description_ChoicesArray = Organization_Description_Choices.split('|')
		Organization_Description_query = reduce(operator.or_, (Q(Organization_Description__icontains = item) for item in Organization_Description_ChoicesArray))

	if(Service_Area_Choices != ""):
		Service_Area_ChoicesArray = Service_Area_Choices.split('|')
		Service_Area_Choices_query = reduce(operator.or_, (Q(Service_Area_Description__icontains = item) for item in Service_Area_ChoicesArray))


	if(organization_structured_Choices != ""):
		organization_structured_ChoicesArray = organization_structured_Choices.split('|')
		organization_structured_Choices_query = reduce(operator.or_, (Q(organization_structured__icontains = item) for item in organization_structured_ChoicesArray))

	if(Activities_Services_Choices != ""):
		Activities_Services_ChoicesArray = Activities_Services_Choices.split('|')
		Activities_Services_Choices_query = reduce(operator.or_, (Q(Activities_Services__icontains = item) for item in Activities_Services_ChoicesArray))

	if(Service_Population_Choices != ""):
		Service_Population_ChoicesArray = Service_Population_Choices.split('|')
		Service_Population_Choices_query = reduce(operator.or_, (Q(Service_Population__icontains = item) for item in Service_Population_ChoicesArray))

	if(Languages_Choices != ""):
		Languages_ChoicesArray = Languages_Choices.split('|')
		Languages_Choices_query = reduce(operator.or_, (Q(Languages__icontains = item) for item in Languages_ChoicesArray))

	if(Languages_Other == "Other"):
		Languages_Other_query = Q(Languages_Other__isnull = False)

	if(cdadmebership != ""):
		if(cdadmebership == "Yes"):
			cdadmebership_query = Q(CDAD_MemberShip__icontains = "Currently a member")
		else:
			surveyKwargsExclude['CDAD_MemberShip__exact'] = "Currently a member"

	if(Council_District_Choices != ""):
		Council_District_ChoicesArray = Council_District_Choices.split('|')
		Council_District_Choices_query = reduce(operator.or_, (Q(CouncilDistricts__icontains = item) for item in Council_District_ChoicesArray))

	if(keyword != ""):
		fields = [f for f in SurveyPanel._meta.fields if isinstance(f, TextField)]
		queries = [Q(**{"%s__icontains" % f.name: keyword}) for f in fields]
		for query in queries:
			keyword_query = keyword_query | query       

	# reduce Service Areas and Council Districts with or
	sa_co_list = [Service_Area_Choices_query, Council_District_Choices_query]
	sa_co_or = reduce(operator.or_, sa_co_list)

	# create query list from the queries that exist from above
	q_list = [Organization_Description_query, organization_structured_Choices_query, Activities_Services_Choices_query, Service_Population_Choices_query, Languages_Choices_query, Languages_Other_query, cdadmebership_query, keyword_query, verified_query, sa_co_or]
	query = reduce(operator.and_, q_list)
	
	# get all survey panel objects that meet the search criteria
	surveys = SurveyPanel.objects.filter(query).exclude(**surveyKwargsExclude)
 
	#build query
	kwargs = {}
	# add returned surveys to location search
	kwargs['Organization_Name_SurveyPanel_FK__in'] = surveys
 
	#get locations
	locations = LocationPanel.objects.filter(**kwargs).order_by('Organization_Name')

	# create Activity list
	for location in locations:
		location.Activity = location.Activity.strip('[]').replace("u'","").replace("'","").split(', ')
		if location.KeepPrivate:
			location.Address = ''

	# figure out which Surveys have geojsons
	surveys_with_maps_ids = []
	for location in locations:
		survey = SurveyPanel.objects.get(Organization_Name=location.Organization_Name_SurveyPanel_FK)
		if survey.MapDissolve:
			surveys_with_maps_ids.append(survey.id)

	surveys_with_maps_ids = set(surveys_with_maps_ids)
	surveys_with_maps_ids = list(surveys_with_maps_ids)

	# load template requested 
	template = request.GET.get("template","")
	if (template == "locations"):
		renderTemplate = 'cdadmap/locations-geojson.html'
	elif (template == "popup"):
		renderTemplate = 'cdadmap/popup-content.html'
	else:
		renderTemplate = 'cdadmap/org-modal.html'

			
	context_dict = {'locations': locations, 'surveys_with_maps_ids':surveys_with_maps_ids}
	return render(request, renderTemplate, context_dict)


# survey views
@login_required
def surveyPage1(request, id=None):

	if id:
		surveyObject = SurveyPanel.objects.get(id=id)
		# get survey name 
		previous_name = surveyObject.Organization_Name
		# check for non superusers and redirect to their dashboard if the user doesn't own the object
		if request.user.groups.filter(name="superusers").exists():
			empty = {}
		else:
			surveyObjectCheck = SurveyPanel.objects.get(user=request.user, removed=False)
			if surveyObject != surveyObjectCheck:
				#send them back to their dashboard
				return HttpResponseRedirect('/dashboard/')
	else:
		surveyObject = SurveyPanel()

	# A HTTP POST?
	if request.method == 'POST':
		form = Page1Form(request.POST, instance=surveyObject)

		# Have we been provided with a valid form?
		if form.is_valid():
			# Save the new data to the database.
			f = form.save(commit=False)

			# if records already exist, loop through them and change the organization name
			if id:
				lookupLocations = LocationPanel.objects.filter(Organization_Name=previous_name)
				for rec in lookupLocations:
					rec.Organization_Name = f.Organization_Name
					rec.Organization_Name_SurveyPanel_FK = None
					rec.save()

				lookupContacts = ContactPanel.objects.filter(Organization_Name=previous_name)
				for rec in lookupContacts:
					rec.Organization_Name = f.Organization_Name
					rec.save()

				lookupMeetings = MeetingPanel.objects.filter(Organization_Name=previous_name)
				for rec in lookupMeetings:
					rec.Organization_Name = f.Organization_Name
					rec.save()

			# add current user
			f.user = request.user
			# mark as draft
			f.verified = False
			f.completed = False
			f.save()

			lookupObject = SurveyPanel.objects.get(Organization_Name=f.Organization_Name)

			# add FK relationship back to survey from location if these exist
			if id:
				lookupLocations = LocationPanel.objects.filter(Organization_Name=lookupObject.Organization_Name)
				for rec in lookupLocations:
					rec.Organization_Name_SurveyPanel_FK = lookupObject
					rec.save()	

			
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
def adminSurveyPage1(request, id=None):

	if id:
		surveyObject = SurveyPanel.objects.get(id=id)
		# get survey name 
		previous_name = surveyObject.Organization_Name
		# check for non superusers and redirect to their dashboard if the user doesn't own the object
		if request.user.groups.filter(name="superusers").exists():
			empty = {}
		else:
			#send any non-superuser back to the dahsboard
			return HttpResponseRedirect('/dashboard/')

	else:
		surveyObject = SurveyPanel()

	# A HTTP POST?
	if request.method == 'POST':
		form = AdminPage1Form(request.POST, instance=surveyObject)

		# Have we been provided with a valid form?
		if form.is_valid():
			# Save the new data to the database.
			f = form.save(commit=False)

			# if records already exist, loop through them and change the organization name
			if id:
				lookupLocations = LocationPanel.objects.filter(Organization_Name=previous_name)
				for rec in lookupLocations:
					rec.Organization_Name = f.Organization_Name
					rec.Organization_Name_SurveyPanel_FK = None
					rec.save()

				lookupContacts = ContactPanel.objects.filter(Organization_Name=previous_name)
				for rec in lookupContacts:
					rec.Organization_Name = f.Organization_Name
					rec.save()

				lookupMeetings = MeetingPanel.objects.filter(Organization_Name=previous_name)
				for rec in lookupMeetings:
					rec.Organization_Name = f.Organization_Name
					rec.save()

			# Save the new data to the database.
			f = form.save(commit=True)

			lookupObject = SurveyPanel.objects.get(Organization_Name=f.Organization_Name)

			# add FK relationship back to survey from location if these exist
			if id:
				lookupLocations = LocationPanel.objects.filter(Organization_Name=lookupObject.Organization_Name)
				for rec in lookupLocations:
					rec.Organization_Name_SurveyPanel_FK = lookupObject
					rec.save()		

			return HttpResponseRedirect(reverse('surveyPage2', args=(lookupObject.pk,)))
		else:
			# The supplied form contained errors - just print them to the terminal.
			print form.errors
	else:
		# If the request was not a POST, display the form to enter details.
		form = AdminPage1Form(instance=surveyObject)

	# Bad form (or form details), no form supplied...
	# Render the form with error messages (if any).
	return render(request, 'cdadsurvey/surveyPage1.html', {'form': form})



@login_required
def surveyPage2(request, id=None, passed=False):

	surveyObject = SurveyPanel.objects.get(id=id)
	# check for non superusers and redirect to their dashboard if the user doesn't own the object
	is_su = request.user.groups.filter(name='superusers').exists()
	if is_su:
		empty = {}
	else:
		surveyObjectCheck = SurveyPanel.objects.get(user=request.user)
		if surveyObject != surveyObjectCheck:
			#send them back to their dashboard
			return HttpResponseRedirect('/dashboard/')


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
	return render(request, 'cdadsurvey/surveyPage2.html', {'form': form, 'id':id, 'is_su': is_su})


@login_required
def surveyPage3(request, id=None, passed=False):

	surveyObject = SurveyPanel.objects.get(id=id)
	# check for non superusers and redirect to their dashboard if the user doesn't own the object
	if request.user.groups.filter(name="superusers").exists():
		empty = {}
	else:
		surveyObjectCheck = SurveyPanel.objects.get(user=request.user)
		if surveyObject != surveyObjectCheck:
			#send them back to their dashboard
			return HttpResponseRedirect('/dashboard/')

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
	# check for non superusers and redirect to their dashboard if the user doesn't own the object
	if request.user.groups.filter(name="superusers").exists():
		empty = {}
	else:
		surveyObjectCheck = SurveyPanel.objects.get(user=request.user)
		if surveyObject != surveyObjectCheck:
			#send them back to their dashboard
			return HttpResponseRedirect('/dashboard/')

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
	base_url = "https://maps.googleapis.com/maps/api/geocode/json?"

	surveyObject = SurveyPanel.objects.get(id=id)
	# check for non superusers and redirect to their dashboard if the user doesn't own the object
	if request.user.groups.filter(name="superusers").exists():
		empty = {}
	else:
		surveyObjectCheck = SurveyPanel.objects.get(user=request.user)
		if surveyObject != surveyObjectCheck:
			#send them back to their dashboard
			return HttpResponseRedirect('/dashboard/')

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
						params = { 'address' : fullAddress, 'key' : GEOCODER_API_KEY }                    
					else:
						fullAddress = instance.Address + ', ' + instance.State
						params = { 'address' : fullAddress, 'key' : GEOCODER_API_KEY }

					# fully form url    
					request_url = base_url + urllib.urlencode(params)
					
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
	# check for non superusers and redirect to their dashboard if the user doesn't own the object
	if request.user.groups.filter(name="superusers").exists():
		empty = {}
	else:
		surveyObjectCheck = SurveyPanel.objects.get(user=request.user)
		if surveyObject != surveyObjectCheck:
			#send them back to their dashboard
			return HttpResponseRedirect('/dashboard/')

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
	# check for non superusers and redirect to their dashboard if the user doesn't own the object
	if request.user.groups.filter(name="superusers").exists():
		empty = {}
	else:
		surveyObjectCheck = SurveyPanel.objects.get(user=request.user)
		if surveyObject != surveyObjectCheck:
			#send them back to their dashboard
			return HttpResponseRedirect('/dashboard/')

	return render(request, 'cdadsurvey/surveyPage7.html', {'surveyObject': surveyObject, 'id':id, 'GEOCODER_API_KEY':GEOCODER_API_KEY})


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
	# check for non superusers and redirect to their dashboard if the user doesn't own the object
	if request.user.groups.filter(name="superusers").exists():
		empty = {}
	else:
		surveyObjectCheck = SurveyPanel.objects.get(user=request.user)
		if surveyObject != surveyObjectCheck:
			#send them back to their dashboard
			return HttpResponseRedirect('/dashboard/')

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
	# check for non superusers and redirect to their dashboard if the user doesn't own the object
	if request.user.groups.filter(name="superusers").exists():
		empty = {}
	else:
		surveyObjectCheck = SurveyPanel.objects.get(user=request.user)
		if surveyObject != surveyObjectCheck:
			#send them back to their dashboard
			return HttpResponseRedirect('/dashboard/')

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
	# check for non superusers and redirect to their dashboard if the user doesn't own the object
	if request.user.groups.filter(name="superusers").exists():
		empty = {}
	else:
		surveyObjectCheck = SurveyPanel.objects.get(user=request.user)
		if surveyObject != surveyObjectCheck:
			#send them back to their dashboard
			return HttpResponseRedirect('/dashboard/')

	# creating a CSV string from a Python list
	if surveyObject.Languages_Other:
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
	# check for non superusers and redirect to their dashboard if the user doesn't own the object
	if request.user.groups.filter(name="superusers").exists():
		empty = {}
	else:
		surveyObjectCheck = SurveyPanel.objects.get(user=request.user)
		if surveyObject != surveyObjectCheck:
			#send them back to their dashboard
			return HttpResponseRedirect('/dashboard/')

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
	# check for non superusers and redirect to their dashboard if the user doesn't own the object
	if request.user.groups.filter(name="superusers").exists():
		empty = {}
	else:
		surveyObjectCheck = SurveyPanel.objects.get(user=request.user)
		if surveyObject != surveyObjectCheck:
			#send them back to their dashboard
			return HttpResponseRedirect('/dashboard/')

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
	# check for non superusers and redirect to their dashboard if the user doesn't own the object
	if request.user.groups.filter(name="superusers").exists():
		empty = {}
	else:
		surveyObjectCheck = SurveyPanel.objects.get(user=request.user)
		if surveyObject != surveyObjectCheck:
			#send them back to their dashboard
			return HttpResponseRedirect('/dashboard/')

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

			# add newly added partners to the list of partners for this survey
			for f in formset:
				#look up partner
				if 'partner_name' in f.cleaned_data.keys():
					newPartner = Partners.objects.get(partner_name=f.cleaned_data['partner_name'])
					surveyObject.partners.add(newPartner)


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
	# check for non superusers and redirect to their dashboard if the user doesn't own the object
	if request.user.groups.filter(name="superusers").exists():
		empty = {}
	else:
		surveyObjectCheck = SurveyPanel.objects.get(user=request.user)
		if surveyObject != surveyObjectCheck:
			#send them back to their dashboard
			return HttpResponseRedirect('/dashboard/')

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

	surveyObject = SurveyPanel.objects.get(id=id)
	# check for non superusers and redirect to their dashboard if the user doesn't own the object
	if request.user.groups.filter(name="superusers").exists():
		empty = {}
	else:
		surveyObjectCheck = SurveyPanel.objects.get(user=request.user)
		if surveyObject != surveyObjectCheck:
			#send them back to their dashboard
			return HttpResponseRedirect('/dashboard/')

	# A HTTP POST?
	if request.method == 'POST':
		# set survey to comleted status
		form = Page15Form(request.POST, instance=surveyObject)

		# Have we been provided with a valid form?
		if form.is_valid():
			# set to complted
			f = form.save(commit=False)
			f.completed = True
			f.save()

			# send email to the user that their record has been submitted and CDAD will verify
			subject = "Survey Submitted to d[COM]munity!"
			html_message = "Dear "+ surveyObject.Survey_Taker_Name +",<br /><br />Thank you for completing the survey and adding your organization, " + surveyObject.Organization_Name + " to the d[COM]munity system! A representative from CDAD will review your survey submission shortly, and you will receieve an email at this address when your information is avialable on the d[COM]munity website.<br /><br />Again, thank you for being a part of d[COM]munity and please contact us with any questions!<br /><br /><a href=\"http://cdad-online.org/\">Community Development Advocates of Detroit</a><br />440 Burroughs St. Suite 340<br />Detroit, MI 48202<br />313-832-4620<br />dcommunity@cdad-online.org"
			message = "Dear "+ surveyObject.Survey_Taker_Name +", Thank you for completing the survey and adding your organization, " + surveyObject.Organization_Name + " to the d[COM]munity system! A representative from CDAD will review your survey submission shortly, and you will receieve an email at this address when your information is avialable on the d[COM]munity website. Again, thank you for being a part of d[COM]munity and please contact us with any questions! Community Development Advocates of Detroit, http://cdad-online.org/, 440 Burroughs St. Suite 340, Detroit, MI 48202; 313-832-4620; dcommunity@cdad-online.org"

			send_mail(subject, message, 'dcommunity@cdad-online.org', [surveyObject.Survey_Taker_Email_Address], fail_silently=True, html_message=html_message)

			# send another email to CDAD superusers
			group = Group.objects.get(name='superusers')
			superusers = group.user_set.all()
			for	superuser in superusers:
				subject = "New Survey from "+ surveyObject.Organization_Name +" Submitted to d[COM]munity!"
				html_message = "Dear "+ superuser.first_name +" "+ superuser.last_name +",<br /><br />The group, " + surveyObject.Organization_Name + " just submitted their completed survey to CDAD for their review. Please log in to the d[COM]munity system when you have a moment and verify their work.<br /><br />Thank you!"
				message = "Dear "+ superuser.first_name +" "+ superuser.last_name +", The group, " + surveyObject.Organization_Name + " just submitted their completed survey to CDAD for their review. Please log in to the d[COM]munity system when you have a moment and verify their work. Thank you!"

				send_mail(subject, message, 'dcommunity@cdad-online.org', [superuser.email], fail_silently=True, html_message=html_message)

			return HttpResponseRedirect('/dashboard/')

		else:
			# The supplied form contained errors - just print them to the terminal.
			print form.errors


	else:
		# If the request was not a POST, display the form to enter details.
		form = Page15Form()

	return render(request, 'cdadsurvey/surveyfinish.html', {'id':id, 'form':form})

@login_required
def dashboard(request):

	if request.user.groups.filter(name="superadmin").exists() or request.user.groups.filter(name="superusers").exists():
		# pull all surveys and place them in a sortable table
		surveyObjects = SurveyPanel.objects.all().order_by('Organization_Name')

		return render(request, 'cdadsurvey/admin_dashboard.html', {'surveyObjects':surveyObjects})

	else:

		#are they actively working on a survey
		surveyObjects = SurveyPanel.objects.filter(user=request.user).exclude(removed=True)
		surveyObjectsCount = len(surveyObjects)
		if surveyObjectsCount > 0:
			surveyObject = SurveyPanel.objects.get(user=request.user, removed=False)
			id = surveyObject.id
			page = -99
			update = False
			completed = False
			# is the survey verified? -- if so just give them the update button
			if surveyObject.verified:
				update = True
			else:
				update = False

				# is the survey completed, but not yet verified
				if surveyObject.completed:
					completed = True
				else:
					completed = False

				# look up meeting, contact and location
				meetingObjects = MeetingPanel.objects.filter(Organization_Name=surveyObject.Organization_Name)
				meetingObjectsCount = len(meetingObjects)
				locationObjects = LocationPanel.objects.filter(Organization_Name=surveyObject.Organization_Name)
				locationObjectsCount = len(locationObjects)
				contactObjects = ContactPanel.objects.filter(Organization_Name=surveyObject.Organization_Name)
				contactObjectsCount = len(contactObjects)

				#where in the survey are they? -- going back to front
				if completed:
					page = 15
				elif surveyObject.partners.count() > 0:
					page = 14
				elif surveyObject.accomplish_one_title:
					page = 13
				elif meetingObjectsCount > 0:
					page = 12
				elif surveyObject.Service_Population:
					page = 11
				elif surveyObject.Activities_Services:
					page = 10
				elif surveyObject.organization_structured:
					page = 9
				elif surveyObject.MapDissolve:
					page = 8
				elif surveyObject.Service_Area_Description:
					page = 7
				elif locationObjectsCount > 0:
					page = 6
				elif contactObjectsCount > 0:
					page = 5
				elif surveyObject.Social_Email:
					page = 4
				elif surveyObject.Year_Founded:
					page = 3
				elif surveyObject.Organization_Name:
					page = 2
				else:
					page = 1


		else:
			#no, then redirect to the survey page to start survey
			return HttpResponseRedirect('/survey/')


		return render(request, 'cdadsurvey/provider_dashboard.html', {'update':update, 'completed':completed, 'id':id, 'page':page, 'surveyObject':surveyObject})

@login_required
def verifysurvey(request, id=None):

	if request.user.groups.filter(name="superusers").exists():
		surveyObject = SurveyPanel.objects.get(id=id)

		surveyObject.Organization_Description = surveyObject.Organization_Description.strip('[]').replace("u'","").replace("'","").split(', ')
		surveyObject.Organization_Description = ", ".join(str(lang) for lang in surveyObject.Organization_Description)

		# A HTTP POST?
		if request.method == 'POST':
			form = VerifyForm(request.POST, instance=surveyObject)

			# Have we been provided with a valid form?
			if form.is_valid():
				# Save the new data to the database.
				f = form.save(commit=True)

				if f.verified:
					#email user
					subject = "d[COM]munity Survey Verified!"
					html_message = "Dear "+ surveyObject.Survey_Taker_Name +",<br /><br />The survey you submitted for " + surveyObject.Organization_Name + " to the d[COM]munity system has been verified by CDAD and will now appear on the <a href=\"http://cdad-online.org/dcommunity/\">d[COM]munity website</a>. Please visit <a href=\"http://cdad-online.org/dcommunity/\">http://cdad-online.org/dcommunity/</a> to see your information displayed in our mapping tool. Again, we appreciate your time and energy in completing our survey.<br /><br />Thank you for being a part of d[COM]munity and please contact us with any questions!<br /><br /><a href=\"http://cdad-online.org/\">Community Development Advocates of Detroit</a><br />440 Burroughs St. Suite 340<br />Detroit, MI 48202<br />313-832-4620<br />dcommunity@cdad-online.org"
					message = "Dear "+ surveyObject.Survey_Taker_Name +", The survey you submitted for " + surveyObject.Organization_Name + " to the d[COM]munity system has been verified by CDAD and will now appear on the d[COM]munity website. Please visit http://cdad-online.org/dcommunity/ to see your information displayed in our mapping tool. Again, we appreciate your time and energy in completing our survey. Thank you for being a part of d[COM]munity and please contact us with any questions! Community Development Advocates of Detroit; http://cdad-online.org/; 440 Burroughs St. Suite 340, Detroit, MI 48202; 313-832-4620; dcommunity@cdad-online.org"

					send_mail(subject, message, 'dcommunity@cdad-online.org', [surveyObject.Survey_Taker_Email_Address], fail_silently=True, html_message=html_message)

				return HttpResponseRedirect('/dashboard/')
			else:
				# The supplied form contained errors - just print them to the terminal.
				print form.errors
		else:
			# If the request was not a POST, display the form to enter details.
			form = VerifyForm(instance=surveyObject)

		# Bad form (or form details), no form supplied...
		# Render the form with error messages (if any).
		return render(request, 'cdadsurvey/verifysurvey.html', {'form': form, 'surveyObject': surveyObject, 'id':id})



	else:
		return HttpResponseRedirect('/dashboard/')


@login_required
def removesurvey(request, id=None):

	if request.user.groups.filter(name="superusers").exists():
		surveyObject = SurveyPanel.objects.get(id=id)

		surveyObject.Organization_Description = surveyObject.Organization_Description.strip('[]').replace("u'","").replace("'","").split(', ')
		surveyObject.Organization_Description = ", ".join(str(lang) for lang in surveyObject.Organization_Description)

		# A HTTP POST?
		if request.method == 'POST':
			form = RemoveForm(request.POST, instance=surveyObject)

			# Have we been provided with a valid form?
			if form.is_valid():
				# Save the new data to the database.
				f = form.save(commit=False)
				f.verified = False
				f.completed = False
				f.save()

				return HttpResponseRedirect('/dashboard/')
			else:
				# The supplied form contained errors - just print them to the terminal.
				print form.errors
		else:
			# If the request was not a POST, display the form to enter details.
			form = RemoveForm(instance=surveyObject)

		# Bad form (or form details), no form supplied...
		# Render the form with error messages (if any).
		return render(request, 'cdadsurvey/removesurvey.html', {'form': form, 'surveyObject': surveyObject, 'id':id})

	else:
		return HttpResponseRedirect('/dashboard/')


@login_required
def removesurveyyep(request, id=None):

	if request.user.groups.filter(name="superusers").exists():
		surveyObject = SurveyPanel.objects.get(id=id)
		locations = LocationPanel.objects.filter(Organization_Name=surveyObject.Organization_Name)
		meetings = MeetingPanel.objects.filter(Organization_Name=surveyObject.Organization_Name)
		contacts = ContactPanel.objects.filter(Organization_Name=surveyObject.Organization_Name)

		surveyObject.delete()

		for location in locations:
			location.delete()

		for meeting in meetings:
			meeting.delete()

		for contact in contacts:
			contact.delete()

		return HttpResponseRedirect('/dashboard/')

	else:
		return HttpResponseRedirect('/dashboard/')




@login_required
def adminRegister(request):

	# A HTTP POST?
	if request.method == 'POST':
		form = AdminUserOverrideCreationForm(request.POST)

		# Have we been provided with a valid form?
		if form.is_valid():
			# Save the new data to the database.
			user = form.save()
			# ensure user is part of the superusers group
			g = Group.objects.get(name='superusers') 
			g.user_set.add(user)

			return HttpResponseRedirect('/dashboard/')
		else:
			# The supplied form contained errors - just print them to the terminal.
			print form.errors
	else:
		# If the request was not a POST, display the form to enter details.
		form = AdminUserOverrideCreationForm()

	# Bad form (or form details), no form supplied...
	# Render the form with error messages (if any).
	return render(request, 'registration/admin_register.html', {'form': form})


@login_required
def administerAccounts(request, id=None):

	if request.user.groups.filter(name="superadmin").exists():
		# pull all users
		users = User.objects.all().exclude(username=request.user)

		for user in users:
			# look up related surveys
			surveys = SurveyPanel.objects.filter(user=user)
			user.surveys = surveys

		return render(request, 'cdadsurvey/super_admin_user_admin.html', {'users': users})
	else:

		return HttpResponseRedirect('/dashboard/')


@login_required
def removeUsers(request, id=None):

	if request.user.groups.filter(name="superadmin").exists():
		userObject = User.objects.get(id=id)

		surveys = SurveyPanel.objects.filter(user=userObject)
		userObject.surveys = surveys

		return render(request, 'cdadsurvey/removeuser.html', {'userObject': userObject})

	else:
		return HttpResponseRedirect('/dashboard/')


def removeUsersYep(request, id=None):

	if request.user.groups.filter(name="superadmin").exists():
		userObject = User.objects.get(id=id)
		surveys = SurveyPanel.objects.filter(user=userObject)
		if surveys:
			# don't delete account if survey's exist for this user
			return HttpResponseRedirect('/administeraccounts/')
		elif userObject.groups.filter(name="superadmin").exists():
			#don't delete if superadmin account
			return HttpResponseRedirect('/administeraccounts/')
		else:
			userObject.delete()
			return HttpResponseRedirect('/administeraccounts/')

	else:
		return HttpResponseRedirect('/dashboard/')


def downloaddata(request):

	#folder for zip file
	folder = "/downloads/"
	filename = "geojsons.zip"

	if not os.path.exists(MEDIA_ROOT + folder):
		os.makedirs(MEDIA_ROOT + folder)

	#create zip file of geojsons
	with zipfile.ZipFile(MEDIA_ROOT + folder + filename, "w", allowZip64=True) as myzip:

		surveys = SurveyPanel.objects.all()
		for survey in surveys:		
			if survey.MapDissolve:
				# temporarily stick a file at the media root
				filename = str(survey.Organization_Name).replace(" ", "_")
				with open(MEDIA_ROOT + "/" + filename + ".geojson", "wb") as myfile:
					myfile.write(survey.MapDissolve)

				myzip.write(MEDIA_ROOT + '/' + filename + ".geojson", "geojsons/" + filename + ".geojson")


				os.remove(MEDIA_ROOT + "/" + filename + ".geojson")

	#create csv file
	with open(MEDIA_ROOT + folder + 'survey_data.csv', 'wb') as f:
		writer = csv.writer(f, quoting=csv.QUOTE_ALL)
		#header row
		headerRow = ['id','user','verified','removed', 'Organization_Name', 'Organizaton_Acronym', 'Survey_Taker_Name', 'Survey_Taker_Email_Address', 'Survey_Taker_Email_AddToList', 'Organization_Description', 'Year_Founded', 'Organization_Logo_Image', 'Organizational_Mission', 'Social_Email', 'AddSocial_Email', 'Social_Phone', 'Social_Phone_KeepPrivate', 'Social_facebook', 'Social_website', 'Social_Twitter', 'Social_other_media', 'Service_Area_Description', 'Service_Area_Geographic_Boundaries', 'CouncilDistricts', 'organization_structured', 'governance_board', 'No_of_board_members', 'staff_members', 'Activities_Services', 'Service_Population', 'Languages', 'Languages_Other', 'accomplish_one_title', 'accomplish_one_description', 'accomplish_two_title', 'accomplish_two_description', 'accomplish_three_title', 'accomplish_three_description', 'accomplish_four_title', 'accomplish_four_description', 'accomplish_five_title', 'accomplish_five_description', 'CDAD_MemberShip', 'CDAD_Services', 'CDAD_Services_Other', 'CDAD_Comments', 'CDAD_FeedBack', 'created', 'modified', 'completed']
		writer.writerow(headerRow)
		surveys = SurveyPanel.objects.all()
		for survey in surveys:
			#empty list for a row
			row = ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','']
			row[0] = survey.id
			row[1] = survey.user
			row[2] = survey.verified
			row[3] = survey.removed
			if survey.Organization_Name:
				row[4] = survey.Organization_Name.encode('ascii', 'ignore')
			else:
				row[4] = ''
			if survey.Organizaton_Acronym:
				row[5] = survey.Organizaton_Acronym.encode('ascii', 'ignore')
			else:
				row[5] = ''
			if survey.Survey_Taker_Name:
				row[6] = survey.Survey_Taker_Name.encode('ascii', 'ignore')
			else:
				row[6] = ''
			if survey.Survey_Taker_Email_Address:
				row[7] = survey.Survey_Taker_Email_Address.encode('ascii', 'ignore')
			else:
				row[7] = ''			
			if survey.Survey_Taker_Email_AddToList:
				row[8] = survey.Survey_Taker_Email_AddToList.encode('ascii', 'ignore')
			else:
				row[8] = ''			
			if survey.Organization_Description:
				row[9] = survey.Organization_Description.encode('ascii', 'ignore')
			else:
				row[9] = ''			
			if survey.Year_Founded:
				row[10] = survey.Year_Founded.encode('ascii', 'ignore')
			else:
				row[10] = ''				
			if survey.Organization_Logo_Image:
				row[11] = survey.Organization_Logo_Image
			else:
				row[11] = ''			
			if survey.Organizational_Mission:
				row[12] = survey.Organizational_Mission.encode('ascii', 'ignore')
			else:
				row[12] = ''			
			if survey.Social_Email:
				row[13] = survey.Social_Email.encode('ascii', 'ignore')
			else:
				row[13] = ''				
			if survey.AddSocial_Email:
				row[14] = survey.AddSocial_Email.encode('ascii', 'ignore')
			else:
				row[14] = ''				
			if survey.Social_Phone:
				row[15] = survey.Social_Phone.encode('ascii', 'ignore')
			else:
				row[15] = ''							
			row[16] = survey.Social_Phone_KeepPrivate
			if survey.Social_facebook:
				row[17] = survey.Social_facebook.encode('ascii', 'ignore')
			else:
				row[17] = ''				
			if survey.Social_website:
				row[18] = survey.Social_website.encode('ascii', 'ignore')
			else:
				row[18] = ''				
			if survey.Social_Twitter:
				row[19] = survey.Social_Twitter.encode('ascii', 'ignore')
			else:
				row[19] = ''
			if survey.Social_other_media:
				row[20] = survey.Social_other_media.encode('ascii', 'ignore')
			else:
				row[20] = ''
			if survey.Service_Area_Description:
				row[21] = survey.Service_Area_Description.encode('ascii', 'ignore')
			else:
				row[21] = ''
			if survey.Service_Area_Geographic_Boundaries:
				row[22] = survey.Service_Area_Geographic_Boundaries.encode('ascii', 'ignore')
			else:
				row[22] = ''			
			if survey.CouncilDistricts:
				row[23] = survey.CouncilDistricts.encode('ascii', 'ignore')
			else:
				row[23] = ''				
			if survey.organization_structured:
				row[24] = survey.organization_structured.encode('ascii', 'ignore')
			else:
				row[24] = ''			
			if survey.governance_board:
				row[25] = survey.governance_board.encode('ascii', 'ignore')
			else:
				row[25] = ''				
			if survey.No_of_board_members:
				row[26] = survey.No_of_board_members.encode('ascii', 'ignore')
			else:
				row[26] = ''			
			if survey.staff_members:
				row[27] = survey.staff_members.encode('ascii', 'ignore')
			else:
				row[27] = ''				
			if survey.Activities_Services:
				row[28] = survey.Activities_Services.encode('ascii', 'ignore')
			else:
				row[28] = ''						
			if survey.Service_Population:
				row[29] = survey.Service_Population.encode('ascii', 'ignore')
			else:
				row[29] = ''			
			if survey.Languages:
				row[30] = survey.Languages.encode('ascii', 'ignore')
			else:
				row[30] = ''			
			if survey.Languages_Other:
				row[31] = survey.Languages_Other.encode('ascii', 'ignore')
			else:
				row[31] = ''			
			if survey.accomplish_one_title:
				row[32] = survey.accomplish_one_title.encode('ascii', 'ignore')
			else:
				row[32] = ''			
			if survey.accomplish_one_description:
				row[33] = survey.accomplish_one_description.encode('ascii', 'ignore')
			else:
				row[33] = ''			
			if survey.accomplish_two_title:
				row[34] = survey.accomplish_two_title.encode('ascii', 'ignore')
			else:
				row[34] = ''			
			if survey.accomplish_two_description:
				row[35] = survey.accomplish_two_description.encode('ascii', 'ignore')
			else:
				row[35] = ''			
			if survey.accomplish_three_title:
				row[36] = survey.accomplish_three_title.encode('ascii', 'ignore')
			else:
				row[36] = ''			
			if survey.accomplish_three_description:
				row[37] = survey.accomplish_three_description.encode('ascii', 'ignore')
			else:
				row[37] = ''				
			if survey.accomplish_four_title:
				row[38] = survey.accomplish_four_title.encode('ascii', 'ignore')
			else:
				row[38] = ''			
			if survey.accomplish_four_description:
				row[39] = survey.accomplish_four_description.encode('ascii', 'ignore')
			else:
				row[39] = ''			
			if survey.accomplish_five_title:
				row[40] = survey.accomplish_five_title.encode('ascii', 'ignore')
			else:
				row[40] = ''				
			if survey.accomplish_five_description:
				row[41] = survey.accomplish_five_description.encode('ascii', 'ignore')
			else:
				row[41] = ''			
			if survey.CDAD_MemberShip:
				row[42] = survey.CDAD_MemberShip.encode('ascii', 'ignore')
			else:
				row[42] = ''				
			if survey.CDAD_Services:
				row[43] = survey.CDAD_Services.encode('ascii', 'ignore')
			else:
				row[43] = ''			
			if survey.CDAD_Services_Other:
				row[44] = survey.CDAD_Services_Other.encode('ascii', 'ignore')
			else:
				row[44] = ''				
			if survey.CDAD_Comments:
				row[45] = survey.CDAD_Comments.encode('ascii', 'ignore')
			else:
				row[45] = ''			
			if survey.CDAD_Comments:
				row[46] = survey.CDAD_FeedBack.encode('ascii', 'ignore')
			else:
				row[46] = ''						
			row[47] = survey.created
			row[48] = survey.modified
			row[49] = survey.completed

			writer.writerow(row)



	return render(request, 'cdadsurvey/downloaddata.html', {})
