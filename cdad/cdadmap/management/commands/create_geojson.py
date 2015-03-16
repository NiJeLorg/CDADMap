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
            # replace whitespace for file names and for geojson
            survey.Organization_Name = survey.Organization_Name.replace("'", "")
             # replace single quotes in file names
            survey.Organization_Name_NoSpaces = survey.Organization_Name.replace(" ", "")
            # replace bad header with correct header
            survey.MapDissolve = survey.MapDissolve.replace('{"paramName":"Arbitrary","dataType":"GPString","value":{"displayFieldName":"","geometryType":"esriGeometryPolygon","spatialReference":{"wkid":4326,"latestWkid":4326},','{ "objectIdFieldName": "objectid","globalIdFieldName": "","geometryType": "esriGeometryPolygon","spatialReference": {"wkid": 4269},')
            
            # remove last bracket
            survey.MapDissolve = survey.MapDissolve[:-1]

            # add in the survey name to the properties in MapDissolve
            survey.MapDissolve = survey.MapDissolve.replace('"fields":[','"fields":[{"name":"OrgName","type":"esriFieldTypeText","alias":"OrgName"},');
            survey.MapDissolve = survey.MapDissolve.replace('{"attributes":{', '{"attributes":{"OrgName":"' + survey.Organization_Name + '",');
            
            # open and create file called OrganizationName without spaces in the file name and a new geojson with ogr2ogr
            with open(os.path.join(__location__, survey.Organization_Name_NoSpaces + "_raw.json"), 'w') as f:
                f.write(survey.MapDissolve)
                
                pathToRaw = os.path.join(__location__,survey.Organization_Name_NoSpaces + "_raw.json")
                pathToNewJson = os.path.join(__location__,survey.Organization_Name_NoSpaces + "_new.json")
                  
                # ogr2ogr -f GeoJSON newfile.json old_file.json OGRGeoJSON                
                command_line = "ogr2ogr -f GeoJSON -t_srs EPSG:4326 " + pathToNewJson + " " + pathToRaw + " OGRGeoJSON"
                args = shlex.split(command_line)
                subprocess.Popen(args)
                                

    def handle(self, *args, **options):
        print "Remove JSON files..."
        self.remove_json_files()
        print "Replace Headers...."
        self.replace_header()







