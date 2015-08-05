import sys,os
from django.core.management.base import BaseCommand, CommandError
from cdadmap.models import *


"""
  Update comma seperated lists to Python lists
"""
class Command(BaseCommand):
    
    def update_surveypanel(self):
            
        for s in SurveyPanel.objects.all():
            # update Organization_Description
            s.Organization_Description = [x.strip() for x in s.Organization_Description.split(',') if x]
            s.Service_Area_Description = [x.strip() for x in s.Service_Area_Description.split(',') if x]
            s.CouncilDistricts = [x.strip() for x in s.CouncilDistricts.split(',') if x]
            s.organization_structured = [x.strip() for x in s.organization_structured.split(',') if x]
            s.Activities_Services = [x.strip() for x in s.Activities_Services.split(',') if x]
            s.Service_Population = [x.strip() for x in s.Service_Population.split(',') if x]
            s.Languages = [x.strip() for x in s.Languages.split(',') if x]
            s.CDAD_MemberShip = [x.strip() for x in s.CDAD_MemberShip.split(',') if x]
            s.CDAD_Services = [x.strip() for x in s.CDAD_Services.split(',') if x]
            s.save()

    def update_locationpanel(self):
            
        for l in LocationPanel.objects.all():
            # update Organization_Description
            l.Activity = [x.strip() for x in l.Activity.split(',') if x]
            l.save()
                                

    def handle(self, *args, **options):
        print "Update SurveyPanel..."
        self.update_surveypanel()
        print "Update LocationPanel..."
        self.update_locationpanel()
        print "Done."







