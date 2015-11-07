from django.db import models
from django import forms
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# import all cdadmap models
from cdadmap.models import *

#date time widget
from datetimewidget.widgets import DateTimeWidget

#add select 2
from django_select2 import *

#date time options
dateTimeOptions = {
'format': 'mm/dd/yyyy HH:ii P',
'autoclose': 'true',
'showMeridian' : 'true',
}

justDateOptions = {
'format': 'mm/dd/yyyy',
'minView': 2,
'autoclose': 'true',
}

YES_NO_CHOICES = (
    ('Yes', 'Yes'),
    ('No', 'No'),
)

ORG_DESCRIPTION_CHOICES = (
    ('Community Development Organization', 'Community Development Organization'),
    ('Advocacy or Social Change Organization', 'Advocacy or Social Change Organization'),
    ('Human Development or Direct Service Organization', 'Human Development or Direct Service Organization'),
    ('Education Related Organization', 'Education Related Organization'),
    ('Neighborhood Association or Block Club', 'Neighborhood Association or Block Club'),
    ('Faith-Based Organization', 'Faith-Based Organization'),
    ('Other', 'Other'),
)

ACTIVITY_CHOICES = (
    ('Youth Programs/Services', 'Youth Programs/Services'),
    ('Senior Programs/Services', 'Senior Programs/Services'),
    ('Health and Wellness Services', 'Health and Wellness Services'),
    ('Entrepreneurship/Business Development Services', 'Entrepreneurship/Business Development Services'),
    ('Job Training', 'Job Training'),
    ('Tutoring and Mentoring', 'Tutoring and Mentoring'),
    ('Computer and/or Technology Resources', 'Computer and/or Technology Resources'),
    ('N/A', 'N/A'),
    ('Other', 'Other'),
)

SERVICE_AREA_CHOICES = (
    ('Council District(s) / Neighborhood(s) / Block(s)', 'Council District(s), Neighborhood(s), or Block(s)'),
    ('City of Detroit', 'City of Detroit'),
    ('Wayne County', 'Wayne County'),
    ('Regional (Metro Detroit)', 'Regional (Metro Detroit)'),
)

GEOGRAPHIC_BOUNDARY_CHOICES = (
    ('Citywide', 'Citywide'),
    ('Specific Geographic Boundaries', 'Specific Geographic Boundaries'),
    ('Both', 'Both'),
)

COUNCIL_DISTRICT_CHOICES = (
    ('Citywide', 'Citywide'),
    ('Council District 1', 'Council District 1'),
    ('Council District 2', 'Council District 2'),
    ('Council District 3', 'Council District 3'),
    ('Council District 4', 'Council District 4'),
    ('Council District 5', 'Council District 5'),
    ('Council District 6', 'Council District 6'),
    ('Council District 7', 'Council District 7'),
)

STRUCTURE_CHOICES = (
    ('Unincorporated / No formal structure', 'Unincorporated / No formal structure'),
    ('501c(3)', '501c(3) (e.g. charitable non-profits)'),
    ('501c(4)', '501c(4) (e.g. advocacy or civic issues non-profits)'),
    ('501c(6)', '501c(6) (e.g. business associations)'),
    ('Community Housing Development Organization (CDHO)', 'Community Housing Development Organization (CDHO)'),
    ('Quasi Governmental', 'Quasi Governmental (DDA, Land Bank, etc.)'),
    ('Governmental Agency', 'Governmental Agency'),
    ('Social Enterprise (L3C)', 'Social Enterprise (L3C)'),
)

STAFF_CHOICES = (
    ('No employees / All volunteer', 'No employees / All volunteer'),
    ('1-5', '1-5'),
    ('6-10', '6-10'),
    ('11-20', '11-20'),
    ('20-50', '20-50'),
    ('More than 50', 'More than 50'),
)

ACTIVITY_SERVICES_CHOICES = (
    ('Housing and/or Commercial Development', 'Housing and/or Commercial Development'),
    ('Community Organizing and Engagement', 'Community Organizing and Engagement'),
    ('Economic Development', 'Economic Development'),
    ('Land Use and/or Community Planning', 'Land Use and/or Community Planning'),
    ('Public Spaces / Parks / Recreation', 'Public Spaces, Parks, or Recreation (e.g. streetscapes, community cleanups, green/open space development)'),
    ('Neighborhood Safety', 'Neighborhood Safety'),
    ('Education', 'Education'),
    ('Youth Services', 'Youth Services'),
    ('Senior Citizen Services', 'Senior Citizen Services'),
    ('Health Care', 'Health Care'),
    ('Community Mental Health', 'Community Mental Health'),
    ('Policy Advocacy and/or Research', 'Policy Advocacy and/or Research'),
    ('Community Gardening / Agriculture / Food Systems', 'Community Gardening, Agriculture and/or Food Systems'),
    ('Labor and/or Workers\' Rights' , 'Labor and/or Workers\' Rights'),
    ('Environmental', 'Environmental'),
    ('Construction / Deconstruction / Demolition', 'Construction, Deconstruction, or Demolition'),
    ('Civil Rights / Civic Society', 'Civil Rights, Civic Society'),
    ('Vacant Property / Blight Removal', 'Vacant Property / Blight Removal'),
    ('Neighborhood Beautification', 'Neighborhood Beautification'),
    ('Property Management', 'Property Management'),
    ('Technology', 'Technology'),
    ('Workforce Development', 'Workforce Development'),
    ('Other', 'Other'),
)


POPULATION_CHOICES = (
    ('Low-income individuals', 'Low-income individuals'),
    ('Moderate-income individuals', 'Moderate-income individuals'),
    ('Children / Youth', 'Children / Youth'),
    ('Homeless', 'Homeless'),
    ('People with Disabilities or Special Needs', 'People with Disabilities or Special Needs'),
    ('Seniors', 'Seniors'),
    ('Immigrants / Refugees / non-English speakers', 'Immigrants, Refugees or non-English speakers'),
    ('Businesses', 'Businesses'),
    ('Job Seekers', 'Job Seekers'),
    ('Schools', 'Schools'),
    ('Neighborhood Residents', 'Neighborhood Residents'),
    ('Neighborhood or Community Groups', 'Neighborhood or Community Groups'),
    ('Faith Institutions', 'Faith Institutions'),
    ('Governmental Institutions', 'Governmental Institutions'),
    ('Other', 'Other'),
)

LANGUAGE_CHOICES = (
    ('English', 'English'),
    ('Spanish', 'Spanish'),
    ('Arabic', 'Arabic'),
)


MEMBERSHIP_CHOICES = (
    ('Currently a member', 'Currently a member'),
    ('Former member and need to renew membership', 'Former member and need to renew membership'),
    ('Interested in learning more about membership', 'Interested in learning more about membership'),
    ('Not interested in membership at this time', 'Not interested in membership at this time'),
)

CDAD_SERVICES_CHOICES = (
    ('Policy Advocacy', 'Policy Advocacy'),
    ('Community / Neighborhood Planning', 'Community/Neighborhood Planning'),
    ('Community Engagement', 'Community Engagement'),
    ('Technical Assitance', 'Technical Assitance'),
    ('Training', 'Training'),
    ('Other', 'Other'),
)

class Page1Form(forms.ModelForm):
    Organizaton_Acronym = forms.CharField(required=False, widget=forms.TextInput(), label="Organizaton Acronym", help_text="e.g. 'CDAD'")
    Survey_Taker_Email_AddToList = forms.ChoiceField(choices=YES_NO_CHOICES, widget=forms.RadioSelect(), label="Add my contact to CDAD\'s email list. You will receive important updates and information from CDAD including our monthly newsletter. (Required)")
    Organization_Description = forms.MultipleChoiceField(choices=ORG_DESCRIPTION_CHOICES, widget=forms.CheckboxSelectMultiple(), label="Organization Description (Required)", help_text="Please choose the one option that best fits. Please only select the Community Development Organization option if your organization fits the CDAD criteria for a Community Development Organization. Please <a href='http://cdad-online.org/membership/membership-categories/' target='_blank'>click here</a> for that description.")

    class Meta:
        model = SurveyPanel
        fields = ('Organization_Name', 'Organizaton_Acronym', 'Survey_Taker_Name', 'Survey_Taker_Email_Address', 'Survey_Taker_Email_AddToList', 'Organization_Description', 'Organization_Description_Other')
        labels = {
            'Organization_Name': 'Organization Name (Required)',
            'Survey_Taker_Name': 'Survey Taker Name (Required)',
            'Survey_Taker_Email_Address': 'Survey Taker Email Address (Required)',
            'Organization_Description_Other': 'If you selected other, please specify', 
        }
        help_texts = {
            'Organization_Name': 'Please enter the full name of your organization. e.g. \'Community Development Advocates of Detroit\'',
            'Survey_Taker_Name': 'e.g. \'John Doe\'',
            'Survey_Taker_Email_Address': 'e.g. \'john@google.com\'',
        }
        widgets = {
            'Organization_Name': forms.widgets.TextInput(),
            'Survey_Taker_Name': forms.widgets.TextInput(),
            'Survey_Taker_Email_Address': forms.widgets.EmailInput(),
            'Organization_Description_Other': forms.widgets.TextInput(),
        }

class CustomUserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        usernameEmail = obj.get_username() + ' (' + obj.email + ')'
        return usernameEmail

class AdminPage1Form(forms.ModelForm):
    user = CustomUserChoiceField(queryset=User.objects.all(), label="Administrators, please select the user in the system that you would like to attach this survey to.")
    Organizaton_Acronym = forms.CharField(required=False, widget=forms.TextInput(), label="Organizaton Acronym", help_text="e.g. 'CDAD'")
    Survey_Taker_Email_AddToList = forms.ChoiceField(choices=YES_NO_CHOICES, widget=forms.RadioSelect(), label="Add my contact to CDAD\'s email list. You will receive important updates and information from CDAD including our monthly newsletter. (Required)")
    Organization_Description = forms.MultipleChoiceField(choices=ORG_DESCRIPTION_CHOICES, widget=forms.CheckboxSelectMultiple(), label="Organization Description (Required)", help_text="Please choose the one option that best fits. Please only select the Community Development Organization option if your organization fits the CDAD criteria for a Community Development Organization. Please <a href='http://cdad-online.org/membership/membership-categories/' target='_blank'>click here</a> for that description.")

    class Meta:
        model = SurveyPanel
        fields = ('user', 'Organization_Name', 'Organizaton_Acronym', 'Survey_Taker_Name', 'Survey_Taker_Email_Address', 'Survey_Taker_Email_AddToList', 'Organization_Description', 'Organization_Description_Other')
        labels = {
            'user': 'Administrators, please select the user in the system that you would like to attach this survey to.',
            'Organization_Name': 'Organization Name (Required)',
            'Survey_Taker_Name': 'Survey Taker Name (Required)',
            'Survey_Taker_Email_Address': 'Survey Taker Email Address (Required)',
            'Organization_Description_Other': 'If you selected other, please specify', 
        }
        help_texts = {
            'Organization_Name': 'Please enter the full name of your organization. e.g. \'Community Development Advocates of Detroit\'',
            'Survey_Taker_Name': 'e.g. \'John Doe\'',
            'Survey_Taker_Email_Address': 'e.g. \'john@google.com\'',
        }
        widgets = {
            'Organization_Name': forms.widgets.TextInput(),
            'Survey_Taker_Name': forms.widgets.TextInput(),
            'Survey_Taker_Email_Address': forms.widgets.EmailInput(),
            'Organization_Description_Other': forms.widgets.TextInput(),
        }




class Page2Form(forms.ModelForm):

    class Meta:
        model = SurveyPanel
        fields = ('Year_Founded', 'Organization_Logo_Image', 'Organizational_Mission')
        labels = {
            'Year_Founded': 'Year Founded (Required)',
            'Organizational_Logo_Image': 'Organization Logo',
            'Organizational_Mission': 'Organization Mission or Purpose (Required)',
        }
        help_texts = {
            'Year_Founded': 'e.g. 1970',
            'Organization_Logo_Image': 'Please upload your organization\'s logo. (.jpg, .jpeg, .png, .gif)',
            'Organizational_Mission': 'Your official mission or a brief explination of what your do.',
        }
        widgets = {
            'Year_Founded': forms.widgets.TextInput(),
        }


class Page3Form(forms.ModelForm):
    AddSocial_Email = forms.ChoiceField(choices=YES_NO_CHOICES, widget=forms.RadioSelect(), label="Add contact to CDAD's email list. You will receive important updates and information from CDAD including our monthly newsletter. (Required)")
    Social_other_media = forms.CharField(required=False, widget=forms.Textarea(), label="Other Social Media Presence", help_text="Please tell us how to find your organization on any other social media platforms (Instagram, Tumblr, YouTube, Next-door, etc.")

    class Meta:
        model = SurveyPanel
        fields = ('Social_Email', 'AddSocial_Email', 'Social_Phone', 'Social_Phone_KeepPrivate', 'Social_website', 'Social_facebook', 'Social_Twitter', 'youtube', 'instagram', 'nextdoor', 'Social_other_media')
        labels = {
            'Social_Email': 'Email Address (Required)',
            'Social_Phone': 'Main Organizational Phone Number (Required)',
            'Social_Phone_KeepPrivate': 'Keep this phone number private',
            'Social_website': 'Website Address',
            'Social_facebook': 'Facebook Page',
            'Social_Twitter': 'Twitter Page',
            'youtube': 'YouTube Channel',
            'instagram': 'Instagram Page',
            'nextdoor': 'Next Door Page',
        }
        help_texts = {
            'Social_Email': 'What is the general email address for contacting your organization?',
            'Social_website': 'How can we find your organization on the web? Please include the full URL including the leading http:// or https://',
            'Social_facebook': 'Please enter your organization\'s Facebook page address. Please include the full URL including the leading http:// or https://',
            'Social_Twitter': 'Please enter your organization\'s Twitter page. Please include the full URL including the leading http:// or https://',
            'youtube': 'Please enter your organization\'s YouTube channel. Please include the full URL including the leading http:// or https://',
            'instagram': 'Please enter your organization\'s Instagram page. Please include the full URL including the leading http:// or https://',
            'nextdoor': 'Please enter your organization\'s Next Door page. Please include the full URL including the leading http:// or https://',
        }
        widgets = {
            'Social_Email': forms.widgets.EmailInput(),
        }



class Page4Form(forms.ModelForm):

    class Meta:
        model = ContactPanel
        fields = ('Name','Title','Tel','KeepPrivateTel','Email','KeepPrivateEmail','AddListPermission')
        labels = {
            'Name': 'Name',
            'Title': 'Title',
            'Tel': 'Telephone Number',
            'Email': 'Email Address',
            'KeepPrivateTel': 'Keep this phone number private',
            'KeepPrivateEmail': 'Keep this email address private',
            'AddListPermission': 'Add this contact to CDAD\'s email list (only check if you have permission to do so)',
        }
        widgets = {
            'Name': forms.widgets.TextInput(),
            'Title': forms.widgets.TextInput(),
            'Tel': forms.widgets.TextInput(),
            'Email': forms.widgets.EmailInput(),
        }


class Page5Form(forms.ModelForm):

    Address2 = forms.CharField(required=False, widget=forms.widgets.TextInput(), label="Address Line 2")
    Activity = forms.MultipleChoiceField(choices=ACTIVITY_CHOICES, widget=forms.CheckboxSelectMultiple(), label="Please indicate any activities or services that take place at this location. (Required)")

    class Meta:
        model = LocationPanel
        fields = ('Address','Address2','City','State','ZipCode','MailingAddress','KeepPrivate','Activity', 'Activity_Other')
        labels = {
            'Address': 'Address',
            'City': 'City',
            'State': 'State',
            'ZipCode': 'Zip Code',
            'MailingAddress': 'This is a mailing address only (e.g. P.O. Box)',
            'KeepPrivate': 'Keep this address private',
            'Activity_Other': 'If you selected other, please specify'
        }
        widgets = {
            'Address': forms.widgets.TextInput(),
            'City': forms.widgets.TextInput(),
            'State': forms.widgets.TextInput(),
            'ZipCode': forms.widgets.TextInput(),
            'Activity_Other': forms.widgets.TextInput(),
        }



class Page6Form(forms.ModelForm):

    Service_Area_Description = forms.MultipleChoiceField(choices=SERVICE_AREA_CHOICES, widget=forms.CheckboxSelectMultiple(), label="Service Area Description (Required)", help_text="How would you describe your organization\'s service area? (Select all that apply)")
    Service_Area_Geographic_Boundaries = forms.ChoiceField(choices=GEOGRAPHIC_BOUNDARY_CHOICES, widget=forms.RadioSelect(), label="In Detroit, does your organization work throughout the whole city or within specific geographic boundaries? (Required)")
    CouncilDistricts = forms.MultipleChoiceField(choices=COUNCIL_DISTRICT_CHOICES, widget=forms.CheckboxSelectMultiple(), label="Please check all of the Detroit City Council Districts in which your organization operates (Required)")

    class Meta:
        model = SurveyPanel
        fields = ('Service_Area_Description','Service_Area_Geographic_Boundaries', 'CouncilDistricts')

class Page8Form(forms.ModelForm):

    organization_structured = forms.MultipleChoiceField(choices=STRUCTURE_CHOICES, widget=forms.CheckboxSelectMultiple(), label="What is your organization\'s legal or administrative structure? (Required)", help_text="Check all that apply")
    governance_board = forms.ChoiceField(choices=YES_NO_CHOICES, widget=forms.RadioSelect(), label="Does your organization have a governance board (e.g. board of directors)? (Required)")
    staff_members = forms.ChoiceField(choices=STAFF_CHOICES, widget=forms.RadioSelect(), label="How many PAID staff members does your organization have? (Required)")

    class Meta:
        model = SurveyPanel
        fields = ('organization_structured','governance_board','No_of_board_members','staff_members')
        labels = {
            'No_of_board_members': 'If yes, how many board members do you have?',
        }
        help_texts = {
            'No_of_board_members': 'This is a required field if your organization has a governance board.'
        }
        widgets = {
            'No_of_board_members': forms.widgets.TextInput(),
        }


class Page9Form(forms.ModelForm):

    Activities_Services = forms.MultipleChoiceField(choices=ACTIVITY_SERVICES_CHOICES, widget=forms.CheckboxSelectMultiple(), label="What are the primary focus areas or your organization\'s activities? (Required)", help_text="Check all that apply")

    class Meta:
        model = SurveyPanel
        fields = ('Activities_Services',)


class Page10Form(forms.ModelForm):

    Service_Population = forms.MultipleChoiceField(choices=POPULATION_CHOICES, widget=forms.CheckboxSelectMultiple(), label="Individuals or Groups Served (Required)")

    Languages = forms.MultipleChoiceField(choices=LANGUAGE_CHOICES, widget=forms.CheckboxSelectMultiple(), label="What languages does your organization provide services in? (Required)")


    class Meta:
        model = SurveyPanel
        fields = ('Service_Population','Service_Population_Other','Languages','Languages_Other')
        labels = {
            'Languages_Other': 'Please add any additional languages your organizaiton provides services in not included above.',
            'Service_Population_Other': 'If you selected other, please specify'
        }
        help_texts = {
            'Languages_Other': 'Please seperate these languages with a comma.'
        }
        widgets = {
            'Languages_Other': forms.widgets.TextInput(),
            'Service_Population_Other': forms.widgets.TextInput(),
        }


class Page11Form(forms.ModelForm):

    StartOn = forms.DateTimeField(widget=DateTimeWidget(options=dateTimeOptions), input_formats=['%m/%d/%Y %I:%M %p'], label="Start Date and Time")
    EndsOn = forms.DateTimeField(widget=DateTimeWidget(options=dateTimeOptions), input_formats=['%m/%d/%Y %I:%M %p'], label="End Date and Time")

    class Meta:
        model = MeetingPanel
        fields = ('hasMeeting','MeetingName','Address','Address2','City','State','ZipCode','StartOn','EndsOn','all_day','repeat','end_repeat','MeetingPerson','MeetingPersonPhone','MeetingPersonEmail')
        labels = {
            'hasMeeting': 'Does your organization hold regular public meetings/events (e.g. monthly block meeting)?',
            'MeetingName': 'Meeting Name',
            'Address': 'Address',
            'Address2': 'Address Line 2',
            'City': 'City',
            'State': 'State',
            'ZipCode': 'Zip Code',
            'all_day': 'All day meeting?',
            'repeat': 'How frequently does this meeting repeat?',
            'end_repeat': 'If the meeting repeat ends, what date does it end on?',
            'MeetingPerson': 'Who should someone contact for more information about this meeting?',
            'MeetingPersonPhone': 'Meeting contact phone number',
            'MeetingPersonEmail': 'Meeting contact email',
        }
        widgets = {
            'MeetingName': forms.widgets.TextInput(),
            'Address': forms.widgets.TextInput(),
            'Address2': forms.widgets.TextInput(),
            'City': forms.widgets.TextInput(),
            'State': forms.widgets.TextInput(),
            'ZipCode': forms.widgets.TextInput(),
            'end_repeat': DateTimeWidget(options=justDateOptions),
            'MeetingPerson': forms.widgets.TextInput(),
            'MeetingPersonPhone': forms.widgets.TextInput(),
            'MeetingPersonEmail': forms.widgets.EmailInput(),
        }


class Page12Form(forms.ModelForm):

    class Meta:
        model = SurveyPanel
        fields = ('accomplish_one_title','accomplish_one_description','accomplish_two_title','accomplish_two_description','accomplish_three_title','accomplish_three_description','accomplish_four_title','accomplish_four_description','accomplish_five_title','accomplish_five_description',)
        labels = {
            'accomplish_one_title': 'Title (Required)',
            'accomplish_one_description': 'Description (Required)',
            'accomplish_two_title': 'Title',
            'accomplish_two_description': 'Description',
            'accomplish_three_title': 'Title',
            'accomplish_three_description': 'Description',
            'accomplish_four_title': 'Title',
            'accomplish_four_description': 'Description',
            'accomplish_five_title': 'Title',
            'accomplish_five_description': 'Description',
        }
        widgets = {
            'accomplish_one_title': forms.widgets.TextInput(),
            'accomplish_two_title': forms.widgets.TextInput(),
            'accomplish_three_title': forms.widgets.TextInput(),
            'accomplish_four_title': forms.widgets.TextInput(),
            'accomplish_five_title': forms.widgets.TextInput(),
        }


class Page13Form(forms.ModelForm):

    class Meta:
        model = SurveyPanel
        fields = ('partners',)
        labels = {
            'partners': 'Select partner organizations from the list below',
        }
        widgets = {
            'partners': widgets.Select2MultipleWidget(),
        }

class AddParner(forms.ModelForm):

    class Meta:
        model = Partners
        fields = ('partner_name',)
        labels = {
            'partner_name': 'Partner Organization Name',
        }


class Page14Form(forms.ModelForm):

    CDAD_MemberShip = forms.ChoiceField(choices=MEMBERSHIP_CHOICES, widget=forms.RadioSelect(), label="Are you a member of CDAD or interested in becoming a member? (Required)")

    CDAD_Services = forms.MultipleChoiceField(choices=CDAD_SERVICES_CHOICES, widget=forms.CheckboxSelectMultiple(), label="How do you believe that CDAD could assist your organization in advancing its work? (Required)")


    class Meta:
        model = SurveyPanel
        fields = ('CDAD_MemberShip','CDAD_Services','CDAD_Services_Other','CDAD_Comments','CDAD_FeedBack',)
        labels = {
            'CDAD_Services_Other': 'If you selected other, please specify',
            'CDAD_Comments': 'Comments',
            'CDAD_FeedBack': 'Feedback',
        }
        help_texts = {
            'CDAD_Comments': 'If there is a specific project or problem for which you are seeking CDAD\'s assistance, please describe it here.',
            'CDAD_FeedBack': 'CDAD would like your feedback on the survey you just completed. Please tell us briefly how easy or difficult is was to complete this survey, noting any strengths and/or weaknesses.',
        }
        widgets = {
            'CDAD_Services_Other': forms.widgets.TextInput(),
        }

class Page15Form(forms.ModelForm):

    class Meta:
        model = SurveyPanel
        fields = ()


class VerifyForm(forms.ModelForm):

    class Meta:
        model = SurveyPanel
        fields = ('verified',)
        labels = {
            'verified': 'Check the box to verify.',
        }


class RemoveForm(forms.ModelForm):

    class Meta:
        model = SurveyPanel
        fields = ('removed',)        
        labels = {
            'removed': 'Check the box to remove this survey.',
        }
        help_texts = {
            'removed': 'Please note that removing this survey doesn not delete it permantly from the database, and it can be recovered at a later date.',
        }


class AdminUserOverrideCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)



