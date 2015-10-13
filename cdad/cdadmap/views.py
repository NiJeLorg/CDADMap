
import sys,os,urllib,urllib2,json,re
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
	kwargs['KeepPrivate__exact'] = False

	#get locations only from verified surveys
	kwargs['Organization_Name_SurveyPanel_FK__verified__exact'] = True

	#get locations 
	locations = LocationPanel.objects.filter(**kwargs).order_by('Organization_Name')

	# create Activity list
	for location in locations:
		location.Activity = location.Activity.strip('[]').replace("u'","").replace("'","").split(', ')

	# figure out which Surveys have geojsons
	surveys_with_maps_ids = []
	for location in locations:
		survey = SurveyPanel.objects.get(Organization_Name=location.Organization_Name_SurveyPanel_FK)
		if survey.MapDissolve:
			surveys_with_maps_ids.append(survey.id)

	surveys_with_maps_ids = set(surveys_with_maps_ids)
	surveys_with_maps_ids = list(surveys_with_maps_ids)
		
	context_dict = {'locations': locations, "Organization_Description_Choices": ORG_DESCRIPTION_CHOICES, "Service_Area_Choices": SERVICE_AREA_CHOICES, "organization_structured_Choices": STRUCTURE_CHOICES, "Activities_Services_Choices": ACTIVITY_SERVICES_CHOICES, "Service_Population_Choices": POPULATION_CHOICES, "Languages_Choices": LANGUAGE_CHOICES, 'surveys_with_maps_ids':surveys_with_maps_ids}
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
	verified_query = Q(verified__exact = True)

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
			cdadmebership_query = Q(CDAD_MemberShip__contains = "Currently a member")
		else:
			surveyKwargsExclude['CDAD_MemberShip__exact'] = "Currently a member"

	if(keyword != ""):
		fields = [f for f in SurveyPanel._meta.fields if isinstance(f, TextField)]
		queries = [Q(**{"%s__contains" % f.name: keyword}) for f in fields]
		for query in queries:
			keyword_query = keyword_query | query       

	# create query list from the queries that exist from above
	q_list = [Organization_Description_query, Service_Area_Choices_query, organization_structured_Choices_query, Activities_Services_Choices_query, Service_Population_Choices_query, Languages_Choices_query, cdadmebership_query, keyword_query, verified_query]
	query = reduce(operator.and_, q_list)
	
	# get all survey panel objects that meet the search criteria
	surveys = SurveyPanel.objects.filter(query).exclude(**surveyKwargsExclude)
 
	#build query
	kwargs = {}
	# add returned surveys to location search
	kwargs['Organization_Name_SurveyPanel_FK__in'] = surveys

	# show only published media
	kwargs['KeepPrivate__exact'] = False
 
	#get locations
	locations = LocationPanel.objects.filter(**kwargs).order_by('Organization_Name')

	# create Activity list
	for location in locations:
		location.Activity = location.Activity.strip('[]').replace("u'","").replace("'","").split(', ')

	# figure out which Surveys have geojsons
	surveys_with_maps_ids = []
	for location in locations:
		survey = SurveyPanel.objects.get(Organization_Name=location.Organization_Name_SurveyPanel_FK)
		if survey.MapDissolve:
			surveys_with_maps_ids.append(survey.id)

	surveys_with_maps_ids = set(surveys_with_maps_ids)
	surveys_with_maps_ids = list(surveys_with_maps_ids)

	# load template requested 
	template = request.GET.get("template","All")
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
def adminSurveyPage1(request, id=None):

	if id:
		surveyObject = SurveyPanel.objects.get(id=id)
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
			f = form.save(commit=True)
			lookupObject = SurveyPanel.objects.get(Organization_Name=f.Organization_Name)
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
	base_url = "http://maps.googleapis.com/maps/api/geocode/json?"

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
		# send email to the user that their record has been submitted and CDAD will verify
		subject = "Survey Submitted to d[COM]munity!"
		html_message = "Dear "+ surveyObject.Survey_Taker_Name +",<br /><br />Thank you for completing the survey and adding your organization, " + surveyObject.Organization_Name + " to the d[COM]munity system! A representative from CDAD will review your survey submission shortly, and you will receieve an email at this address when your information is avialable on the d[COM]munity webesite.<br /><br />Again, thank you!<br />Community Development Advocates of Detroit<br /><a href=\"http://cdad-online.org/\">http://cdad-online.org/</a>"
		message = "Dear "+ surveyObject.Survey_Taker_Name +", Thank you for completing the survey and adding your organization, " + surveyObject.Organization_Name + " to the d[COM]munity system! A representative from CDAD will review your survey submission shortly, and you will receieve an email at this address when your information is avialable on the d[COM]munity webesite. Again, thank you! Community Development Advocates of Detroit, http://cdad-online.org/"

		#send_mail(subject, message, 'dcommunity.cdad@gmail.com', [surveyObject.Survey_Taker_Email_Address], fail_silently=True, html_message=html_message)

		# send another email to CDAD superusers
		group = Group.objects.get(name='superusers')
		superusers = group.user_set.all()
		for	superuser in superusers:
			subject = "New Survey from "+ surveyObject.Organization_Name +" Submitted to d[COM]munity!"
			html_message = "Dear "+ superuser.first_name +" "+ superuser.last_name +",<br /><br />The group, " + surveyObject.Organization_Name + " just submitted their completed survey to CDAD for their review. Please log in to the d[COM]munity system when you have a moment and verify their work.<br /><br />Thank you!"
			message = "Dear "+ superuser.first_name +" "+ superuser.last_name +", The group, " + surveyObject.Organization_Name + " just submitted their completed survey to CDAD for their review. Please log in to the d[COM]munity system when you have a moment and verify their work. Thank you!"

			#send_mail(subject, message, 'dcommunity.cdad@gmail.com', [superuser.email], fail_silently=True, html_message=html_message)

		return HttpResponseRedirect('/dashboard/')
	else:
		# If the request was not a POST, display the form to enter details.
		form = Page15Form()

	return render(request, 'cdadsurvey/surveyfinish.html', {'id':id, 'form':form})

@login_required
def dashboard(request):

	if request.user.groups.filter(name="superusers").exists():
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
			# is the survey verified? -- if so just give them the update button
			if surveyObject.verified:
				update = True
			else:
				update = False

				# look up meeting, contact and location
				meetingObjects = MeetingPanel.objects.filter(Organization_Name=surveyObject.Organization_Name)
				meetingObjectsCount = len(meetingObjects)
				locationObjects = LocationPanel.objects.filter(Organization_Name=surveyObject.Organization_Name)
				locationObjectsCount = len(locationObjects)
				contactObjects = ContactPanel.objects.filter(Organization_Name=surveyObject.Organization_Name)
				contactObjectsCount = len(contactObjects)

				#where in the survey are they? -- going back to front
				if surveyObject.CDAD_MemberShip:
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


		return render(request, 'cdadsurvey/provider_dashboard.html', {'update':update, 'id':id, 'page':page, 'surveyObject':surveyObject})

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
					html_message = "Dear "+ surveyObject.Survey_Taker_Name +",<br /><br />The survey you submitted for " + surveyObject.Organization_Name + " to the d[COM]munity system had been verified by CDAD and will now appear on the d[COM]munity website. Please visit <a href=\"http://cdad-online.org/\">http://cdad-online.org/</a> and click on d[COM]munity to see your information displayed in our mapping tool. Again, thank you for your time and energy in completing our survey!<br /><br />Thank you!<br />Community Development Advocates of Detroit<br /><a href=\"http://cdad-online.org/\">http://cdad-online.org/</a>"
					message = "Dear "+ surveyObject.Survey_Taker_Name +", The survey you submitted for " + surveyObject.Organization_Name + " to the d[COM]munity system had been verified by CDAD and will now appear on the d[COM]munity website. Please visit http://cdad-online.org/ and click on d[COM]munity to see your information displayed in our mapping tool. Again, thank you for your time and energy in completing our survey! Thank you! Community Development Advocates of Detroit, http://cdad-online.org/"

					#send_mail(subject, message, 'dcommunity.cdad@gmail.com', [surveyObject.Survey_Taker_Email_Address], fail_silently=True, html_message=html_message)

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
