import sys,os,urllib,urllib2,json
from django.core.management.base import BaseCommand, CommandError
from cdadmap.models import LocationPanel


"""
  Loads data from MapDissolve field and replaces header text
"""
class Command(BaseCommand):
    
    def geocode_locations(self):
        
    	# get base URL and params for geocoding
    	base_url = "http://maps.googleapis.com/maps/api/geocode/json?";
        
        
        for location in LocationPanel.objects.filter(Address__isnull=False, Lat__isnull=True):
            if bool(location.City) is True:
                fullAddress = location.Address + ' ' + location.City + ', ' + location.State
                params = { 'address' : fullAddress, 'sensor' : "false" }                    
            else:
                fullAddress = location.Address + ', ' + location.State
                params = { 'address' : fullAddress, 'sensor' : "false" }                    
        
            # fully form url    
            request_url = base_url + urllib.urlencode(params);
            
            #send request to google and decode the returned JSON into a string
            response = json.loads(urllib2.urlopen(request_url).read(1000000))
        
            # pull out and save the lat & lons            
            location.Lat = response['results'][0]['geometry']['location']['lat']	    	
            location.Lon = response['results'][0]['geometry']['location']['lng']           
        
            location.save()
                                

    def handle(self, *args, **options):
        print "Geocode Locations..."
        self.geocode_locations()
        print "Done."







