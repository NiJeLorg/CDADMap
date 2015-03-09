import sys,os
from django.core.management.base import BaseCommand, CommandError
from cdadmap.models import *


"""
  Sets the foreign key in locationPanel from SurveyPanel and ContactPanel
"""
class Command(BaseCommand):
    
    def update_urls(self):
            
        for survey in SurveyPanel.objects.all():
            #update website values
            survey.Social_website = survey.Social_website.replace('http://', '')
            survey.Social_website = survey.Social_website.replace('https://', '')
            survey.Social_website = 'http://' + survey.Social_website

            #update facebook url
            survey.Social_facebook = survey.Social_facebook.replace('http://', '')
            survey.Social_facebook = survey.Social_facebook.replace('https://', '')
            survey.Social_facebook = 'http://' + survey.Social_facebook

            #update twitter url
            survey.Social_Twitter = survey.Social_Twitter.replace('http://', '')
            survey.Social_Twitter = survey.Social_Twitter.replace('https://', '')
            survey.Social_Twitter = survey.Social_Twitter.replace('twitter.com/', '')
            survey.Social_Twitter = survey.Social_Twitter.replace('@', '')
            survey.Social_Twitter = 'http://twitter.com/' + survey.Social_Twitter

            #save the survey
            survey.save()
                                

    def handle(self, *args, **options):
        print "Update URLs..."
        self.update_urls()
        print "Done."





