from django.contrib import admin

# Register your models here.
from cdadmap.models import Contact
from cdadmap.models import ContactPanel
from cdadmap.models import Location
from cdadmap.models import LocationPanel
from cdadmap.models import Meeting
from cdadmap.models import MeetingPanel
from cdadmap.models import Survey
from cdadmap.models import SurveyPanel

admin.site.register(Contact)
admin.site.register(ContactPanel)
admin.site.register(Location)
admin.site.register(LocationPanel)
admin.site.register(Meeting)
admin.site.register(MeetingPanel)
admin.site.register(Survey)
admin.site.register(SurveyPanel)
