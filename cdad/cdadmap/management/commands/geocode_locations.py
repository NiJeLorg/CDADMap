import sys,os,urllib,urllib2,json
from django.core.management.base import BaseCommand, CommandError
from cdadmap.models import LocationPanel
import time
from django.conf import settings
GEOCODER_API_KEY = settings.GEOCODER_API_KEY


"""
  Geocodes locations
"""
class Command(BaseCommand):
    
    def geocode_locations(self):
        
    	# get base URL and params for geocoding
    	base_url = "http://maps.googleapis.com/maps/api/geocode/json?"
        
        
        for counter, location in enumerate(LocationPanel.objects.filter(Address__isnull=False, Lat__exact='', Lon__exact='')):
            # ignore location if address is a P.O. Box
            print location
            if "P.O." not in location.Address and "PO" not in location.Address and "error" not in location.Address:

                if bool(location.City) is True:
                    fullAddress = location.Address + ' ' + location.City + ', ' + location.State
                    params = { 'address' : fullAddress, 'key' : GEOCODER_API_KEY }                    
                else:
                    fullAddress = location.Address + ', ' + location.State
                    params = { 'address' : fullAddress, 'key' : GEOCODER_API_KEY }                    
            
                # fully form url    
                request_url = base_url + urllib.urlencode(params)
                
                #send request to google and decode the returned JSON into a string
                response = json.loads(urllib2.urlopen(request_url).read(1000000))
            
                # pull out and save the lat & lons            
                location.Lat = response['results'][0]['geometry']['location']['lat']	    	
                location.Lon = response['results'][0]['geometry']['location']['lng']           
            
                location.save()

            else:
                location.Lat = 0
                location.Lon = 0
                location.save()
            if counter % 10 == 0:
                print "Sleeping at counter" + str(counter)
                time.sleep(20)
                                

    def handle(self, *args, **options):
        print "Geocode Locations..."
        self.geocode_locations()
        print "Done."







