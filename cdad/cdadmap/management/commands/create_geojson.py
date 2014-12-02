import sys,os,subprocess,shlex
from django.core.management.base import BaseCommand, CommandError
from cdadmap.models import SurveyPanel


"""
  Loads data from MapDissolve field and replaces header text
"""
class Command(BaseCommand):
    
    def remove_json_files(self):
        # remove all json files first
        # where json files go
        __location__ = os.path.normpath(os.path.dirname(__file__) + "/../../static/cdadmap/geojson/")
                
        filelist = [ f for f in os.listdir(__location__) if f.endswith(".json") ]

        # change directory to __location__
        os.chdir(__location__)
        
        # remove files
        for f in filelist:
            os.remove(f)
            
    
    def replace_header(self):
        # where json files go
        __location__ = os.path.normpath(os.path.dirname(__file__) + "/../../static/cdadmap/geojson/")
        
        for survey in SurveyPanel.objects.filter(MapDissolve__startswith='{"paramName"'):
            # replace whitespace for file names
            survey.Organization_Name = survey.Organization_Name.replace(" ", "")
            # replace bad header with correct header
            survey.MapDissolve = survey.MapDissolve.replace('{"paramName":"Arbitrary","dataType":"GPString","value":{"displayFieldName":"","geometryType":"esriGeometryPolygon","spatialReference":{"wkid":4326,"latestWkid":4326},','{ "objectIdFieldName": "objectid","globalIdFieldName": "","geometryType": "esriGeometryPolygon","spatialReference": {"wkid": 4269},')
            
            # remove last bracket
            survey.MapDissolve = survey.MapDissolve[:-1]
            
            # open contact.csv and dump into Contact table
            with open(os.path.join(__location__, survey.Organization_Name + '_raw.json'), 'w') as f:
                f.write(survey.MapDissolve)
                
                pathToRaw = os.path.join(__location__,survey.Organization_Name + '_raw.json')
                pathToNewJson = os.path.join(__location__,survey.Organization_Name + '_new.json')
                  
                # ogr2ogr -f GeoJSON newfile.json old_file.json OGRGeoJSON                
                command_line = 'ogr2ogr -f GeoJSON ' + pathToNewJson + ' ' + pathToRaw +  ' OGRGeoJSON'
                args = shlex.split(command_line)
                subprocess.Popen(args)
                                

    def handle(self, *args, **options):
        print "Remove JSON files..."
        self.remove_json_files()
        print "Replace Headers...."
        self.replace_header()







