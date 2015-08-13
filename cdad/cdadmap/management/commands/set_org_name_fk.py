import sys,os
from django.core.management.base import BaseCommand, CommandError
from cdadmap.models import *


"""
  Sets the foreign key in locationPanel from SurveyPanel and ContactPanel
"""
class Command(BaseCommand):
    
    def set_location_fk(self):
            
        for location in LocationPanel.objects.all():
            #clear values first
            location.Organization_Name_SurveyPanel_FK = None
            location.Organization_Name_ContactPanel_M2M = []
            location.Organization_Name_MeetingPanel_M2M = []

            # look up surveypanel and contactpanel objects for foreign key
            print location.Organization_Name
            surveyPanelRecord = SurveyPanel.objects.get(Organization_Name=location.Organization_Name)
            location.Organization_Name_SurveyPanel_FK = surveyPanelRecord
            contactPanelRecords = ContactPanel.objects.filter(Organization_Name=location.Organization_Name)
            for contactPanelRecord in contactPanelRecords:
                location.Organization_Name_ContactPanel_M2M.add(contactPanelRecord)

            meetingPanelRecords = MeetingPanel.objects.filter(Organization_Name=location.Organization_Name)
            for meetingPanelRecord in meetingPanelRecords:
                location.Organization_Name_MeetingPanel_M2M.add(meetingPanelRecord)
            
            location.save()
                                

    def handle(self, *args, **options):
        print "Set FK Location..."
        self.set_location_fk()
        print "Done."







