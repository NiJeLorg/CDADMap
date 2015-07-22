import sys,os
from django.core.management.base import BaseCommand, CommandError
from cdadmap.models import *
import csv


"""
  Loads list for CDAD partners from CSV
"""
class Command(BaseCommand):
    
    def load_partners(self):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        # open partner.csv and dump into Contact table
        with open(os.path.join(__location__, 'list_of_partners.csv'), 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] != 'name': # Ignore the header row, import everything else
                    partner = Partners()
                    partner.partner_name = row[0]
                    partner.save()


    def handle(self, *args, **options):
        print "Loading List of Partners...."
        self.load_partners()




