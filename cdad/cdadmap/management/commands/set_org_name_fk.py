import sys,os
from django.core.management.base import BaseCommand, CommandError
from cdadmap.models import *


"""
  Loads data from MapDissolve field and replaces header text
"""
class Command(BaseCommand):
    
    def set_location_fk(self):
            
        for location in LocationPanel.objects.filter(Organization_Name_SurveyPanel_FK__isnull=True, Organization_Name_ContactPanel_FK__isnull=True):
            # look up surveypanel and contactpanel objects for foreign key
            surveyPanelRecord = SurveyPanel.objects.get(Organization_Name=location.Organization_Name)
            location.Organization_Name_SurveyPanel_FK = surveyPanelRecord
            contactPanelRecord = ContactPanel.objects.get(Organization_Name=location.Organization_Name)
            location.Organization_Name_ContactPanel_FK = contactPanelRecord
            location.save()
                                

    def handle(self, *args, **options):
        print "Set FK Location..."
        self.set_location_fk()
        print "Done."







