from django.db import models
from django import forms

# import all cdadmap models
from cdadmap.models import *

# CDAD forms below
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



class Page1Form(forms.ModelForm):
    Organizaton_Acronym = forms.CharField(required=False, widget=forms.TextInput(), label="Organizaton Acronym", help_text="e.g. 'CDAD'")
    Survey_Taker_Email_AddToList = forms.ChoiceField(choices=YES_NO_CHOICES, widget=forms.RadioSelect(), label="Add my contact to CDAD\'s email list. You will receive important updates and information from CDAD including our monthly newsletter. (Required)")
    Organization_Description = forms.MultipleChoiceField(choices=ORG_DESCRIPTION_CHOICES, widget=forms.CheckboxSelectMultiple(), label="Organization Description (Required)", help_text="Please choose the one option that best fits. Please only select the Community Development Organization option if your organization fits the CDAD criteria for a Community Development Organization. Please <a href='http://cdad-online.org/membership/membership-categories/' target='_blank'>click here</a> for that description.")

    class Meta:
        model = SurveyPanel
        fields = ('Organization_Name', 'Organizaton_Acronym', 'Survey_Taker_Name', 'Survey_Taker_Email_Address', 'Survey_Taker_Email_AddToList', 'Organization_Description')
        labels = {
            'Organization_Name': 'Organization Name (Required)',
            'Survey_Taker_Name': 'Survey Taker Name (Required)',
            'Survey_Taker_Email_Address': 'Survey Taker Email Address (Required)',
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
    Social_website = forms.CharField(required=False, widget=forms.TextInput(), label="Website Address", help_text="How can we find your organization on the web?")
    Social_facebook = forms.CharField(required=False, widget=forms.TextInput(), label="Facebook", help_text="Please enter your organization's Facebook page address or name.")
    Social_Twitter = forms.CharField(required=False, widget=forms.TextInput(), label="Twitter", help_text="Please enter your organization's Twitter \"handle\" or name.")
    Social_other_media = forms.CharField(required=False, widget=forms.Textarea(), label="Other Social Media Presence", help_text="Please tell us how to find your organization on any other social media platforms (Instagram, Tumblr, YouTube, Next-door, etc.")

    class Meta:
        model = SurveyPanel
        fields = ('Social_Email', 'AddSocial_Email', 'Social_website', 'Social_facebook', 'Social_Twitter', 'Social_other_media')
        labels = {
            'Social_Email': 'Email Address (Required)',
        }
        help_texts = {
            'Social_Email': 'What is the general email address for contacting your organization?',
        }
        widgets = {
            'Social_Email': forms.widgets.TextInput(),
        }

class Page4Form(forms.ModelForm):

    class Meta:
        model = SurveyPanel
        fields = ('Service_Area_Description',)
        labels = {
            'Service_Area_Description': 'Stopping Here',
        }
        help_texts = {
            'Service_Area_Description': 'Nothing from here on works yet!',
        }
        widgets = {
            'Service_Area_Description': forms.widgets.TextInput(),
        }