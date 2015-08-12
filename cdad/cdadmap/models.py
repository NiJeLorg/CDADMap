from django.db import models
# import User model
from django.contrib.auth.models import User
import datetime

# CDAD models below

#names of partners
class Partners(models.Model):
    partner_name = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.partner_name        


# Survey model retired
class Survey(models.Model):
    id = models.IntegerField(null=False, primary_key=True)
    Organization_Name = models.TextField()
    Organizaton_Acronym = models.TextField()
    Survey_Taker_Name = models.TextField()
    Survey_Taker_Email_Address = models.TextField()
    Survey_Taker_Email_AddToList = models.TextField()
    Organization_Description = models.TextField()
    Year_Founded = models.TextField()
    Organization_Logo = models.TextField()
    Organizational_Mission = models.TextField()
    Social_Email = models.TextField()
    AddSocial_Email = models.TextField()
    Social_facebook = models.TextField()
    Social_website = models.TextField()
    Social_Twitter = models.TextField()
    Social_other_media = models.TextField()
    Service_Area_Description = models.TextField()
    Service_Area_Geographic_Boundaries = models.TextField()
    MapDissolve = models.TextField()
    organization_structured = models.TextField()
    governance_board = models.TextField()
    No_of_board_members = models.TextField()
    staff_members = models.TextField()
    Activities_Services = models.TextField()
    Service_Population = models.TextField()
    Languages = models.TextField()
    accomplish_one_title = models.TextField()
    accomplish_one_description = models.TextField()
    accomplish_two_title = models.TextField()
    accomplish_two_description = models.TextField()
    accomplish_three_title = models.TextField()
    accomplish_three_description = models.TextField()
    accomplish_four_title = models.TextField()
    accomplish_four_description = models.TextField()
    accomplish_five_title = models.TextField()
    accomplish_five_description = models.TextField()
    CDAD_MemberShip = models.TextField()
    CDAD_Services = models.TextField()
    CDAD_Comments = models.TextField()
    CDAD_FeedBack = models.TextField()
    MyTrace = models.IntegerField(default=0)
        
    class Meta:
        db_table = 'survey'

    def __str__(self):
        return self.Organization_Name        


# Default user for syncing, users can be linked to surveys later
DEFAULT_USER_ID = 1

# SurveyPanel defined first to allow foreign key relationship to come late        
class SurveyPanel(models.Model):
    id = models.IntegerField(null=False, primary_key=True)
    user = models.ForeignKey(User, default=DEFAULT_USER_ID)
    verified = models.BooleanField(default=False)
    removed = models.BooleanField(default=False)
    Organization_Name = models.CharField(max_length=255, default='', unique=True)
    Organizaton_Acronym = models.TextField()
    Survey_Taker_Name = models.TextField()
    Survey_Taker_Email_Address = models.TextField()
    Survey_Taker_Email_AddToList = models.TextField()
    Organization_Description = models.TextField()
    Year_Founded = models.TextField()
    Organization_Logo = models.TextField()
    Organization_Logo_Image = models.ImageField(upload_to="img/%Y_%m_%d_%h_%M_%s", null=True, blank=True)
    Organizational_Mission = models.TextField()
    Social_Email = models.TextField()
    AddSocial_Email = models.TextField()
    Social_Phone = models.CharField(max_length=20, default='')
    Social_Phone_KeepPrivate = models.BooleanField(default=False)
    Social_facebook = models.URLField(max_length=2000, null=True, blank=True)
    Social_website = models.URLField(max_length=2000, null=True, blank=True)
    Social_Twitter = models.URLField(max_length=2000, null=True, blank=True)
    Social_other_media = models.TextField()
    Service_Area_Description = models.TextField()
    Service_Area_Geographic_Boundaries = models.TextField()
    CouncilDistricts = models.TextField()
    MapDissolve = models.TextField()
    organization_structured = models.TextField()
    governance_board = models.TextField()
    No_of_board_members = models.TextField()
    staff_members = models.TextField()
    Activities_Services = models.TextField()
    Service_Population = models.TextField()
    Languages = models.TextField()
    Languages_Other = models.TextField(null=True, blank=True)
    accomplish_one_title = models.TextField()
    accomplish_one_description = models.TextField()
    accomplish_two_title = models.TextField(null=True, blank=True)
    accomplish_two_description = models.TextField(null=True, blank=True)
    accomplish_three_title = models.TextField(null=True, blank=True)
    accomplish_three_description = models.TextField(null=True, blank=True)
    accomplish_four_title = models.TextField(null=True, blank=True)
    accomplish_four_description = models.TextField(null=True, blank=True)
    accomplish_five_title = models.TextField(null=True, blank=True)
    accomplish_five_description = models.TextField(null=True, blank=True)
    CDAD_MemberShip = models.TextField()
    CDAD_Services = models.TextField()
    CDAD_Services_Other = models.TextField(null=True, blank=True)
    CDAD_Comments = models.TextField(null=True, blank=True)
    CDAD_FeedBack = models.TextField(null=True, blank=True)
    partners = models.ManyToManyField(Partners, null=True, blank=True)
        
    class Meta:
        db_table = 'surveyPanel'

    def __str__(self):
        return self.Organization_Name


class Contact(models.Model):
    id = models.IntegerField(null=False, primary_key=True)
    Organization_Name = models.TextField()
    Name = models.TextField()
    Title = models.TextField()
    Tel = models.TextField()
    Email = models.TextField()
    KeepPrivate = models.TextField()
    AddListPermission = models.TextField()
    MyTrace = models.IntegerField(default=0)

    class Meta:
        db_table = 'contact'
        
    def __str__(self):
        return self.Organization_Name
        

class ContactPanel(models.Model):
    id = models.IntegerField(null=False, primary_key=True)
    Organization_Name = models.TextField()
    Name = models.TextField()
    Title = models.TextField()
    Tel = models.TextField()
    Email = models.TextField()
    KeepPrivateTel = models.BooleanField(default=False)
    KeepPrivateEmail = models.BooleanField(default=False)
    AddListPermission = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'contactPanel'

    def __str__(self):
        return self.Organization_Name


class Meeting(models.Model):
    id = models.IntegerField(null=False, primary_key=True)
    Organization_Name = models.TextField()
    hasMeeting = models.TextField()
    MeetingName = models.TextField()
    Address = models.TextField()
    Address2 = models.TextField()
    City = models.TextField()
    ZipCode = models.TextField()
    State = models.TextField()
    Repeat1 = models.TextField()
    RepeatEvery = models.TextField()
    Time1 = models.TextField()
    StartOn = models.TextField()
    EndsOn = models.TextField()
    Occurances = models.TextField()
    On1 = models.TextField()
    MeetingPerson = models.TextField()
    MeetingPersonPhone = models.TextField()
    MeetingPersonEmail = models.TextField()
    MeetAlways = models.TextField()
    MyTrace = models.IntegerField(default=0)

    class Meta:
        db_table = 'meeting'

    def __str__(self):
        return self.Organization_Name

REPEAT_CHOICES = (
    ('NEVER', 'Never'),
    ('DAILY', 'Every Day'),
    ('WEEKDAY', 'Every Weekday'),
    ('WEEKLY', 'Every Week'),
    ('MONTHLY', 'Every Month'),
    ('YEARLY', 'Every Year'),
)


class MeetingPanel(models.Model):
    id = models.IntegerField(null=False, primary_key=True)
    Organization_Name = models.TextField()
    hasMeeting = models.BooleanField(default=False)
    MeetingName = models.TextField()
    Address = models.TextField()
    Address2 = models.TextField(null=True, blank=True)
    City = models.TextField()
    ZipCode = models.TextField()
    State = models.TextField()
    all_day = models.BooleanField(default=False)
    repeat = models.CharField(max_length=15, choices=REPEAT_CHOICES, default='NEVER')
    end_repeat = models.DateField(null=True, blank=True)
    StartOn = models.DateTimeField()
    EndsOn = models.DateTimeField()
    MeetingPerson = models.TextField()
    MeetingPersonPhone = models.TextField()
    MeetingPersonEmail = models.TextField()
    MeetAlways = models.BooleanField(default=False)

    class Meta:
        db_table = 'meetingpanel'

    def __str__(self):
        return self.Organization_Name

    def getStartWeekDay(self):
        day_of_month = self.StartOn.day
        week_number = (day_of_month - 1) // 7 + 1
        if week_number == 1:
            week_number = '1st'
        elif week_number == 2:
            week_number = '2nd'
        elif week_number == 3:
            week_number = '3rd'
        else:
            week_number = week_number + 'th'
        return week_number

    def checkRepeat(self):
        if datetime.datetime.now().day < self.end_repeat.day:
            return True
        return False


class Location(models.Model):
    id = models.IntegerField(null=False, primary_key=True)
    Organization_Name = models.TextField()
    Address = models.TextField()
    Address2 = models.TextField()
    City = models.TextField()
    ZipCode = models.TextField()
    State = models.TextField()
    MailingAddress = models.TextField()
    KeepPrivate = models.TextField()
    Activity = models.TextField()
    MyTrace = models.IntegerField(default=0)

    class Meta:
        db_table = 'location'

    def __str__(self):
        return self.Organization_Name


class LocationPanel(models.Model):
    idlocation = models.IntegerField(null=False, primary_key=True)
    Organization_Name = models.TextField()
    Address = models.TextField()
    Address2 = models.TextField()
    City = models.TextField()
    ZipCode = models.TextField()
    State = models.TextField()
    MailingAddress = models.BooleanField(default=False)
    KeepPrivate = models.BooleanField(default=False)
    Activity = models.TextField()
    Lat = models.CharField(max_length=255, null=False, blank=True, default='')
    Lon = models.CharField(max_length=255, null=False, blank=True, default='')
    Organization_Name_SurveyPanel_FK = models.ForeignKey(SurveyPanel, to_field='Organization_Name', null=True)
    Organization_Name_ContactPanel_M2M = models.ManyToManyField(ContactPanel, null=True)
    Organization_Name_MeetingPanel_M2M = models.ManyToManyField(MeetingPanel, null=True)
    
    class Meta:
        db_table = 'locationPanel'

    def __str__(self):
        return self.Organization_Name
        
    def getSurveyObject(self):
        """
            get survey object linked to this location object
        """
        surveyObject = SurveyPanel.objects.get(Organization_Name=self.Organization_Name_SurveyPanel_FK)
        surveyObject.Organization_Description = surveyObject.Organization_Description.strip('[]').replace("u'","").replace("'","").split(', ')
        surveyObject.Service_Area_Description = surveyObject.Service_Area_Description.strip('[]').replace("u'","").replace("'","").split(', ')
        surveyObject.CouncilDistricts = surveyObject.CouncilDistricts.strip('[]').replace("u'","").replace("'","").split(', ')
        surveyObject.organization_structured = surveyObject.organization_structured.strip('[]').replace("u'","").replace("'","").split(', ')
        surveyObject.Activities_Services = surveyObject.Activities_Services.strip('[]').replace("u'","").replace("'","").split(', ')
        surveyObject.Service_Population = surveyObject.Service_Population.strip('[]').replace("u'","").replace("'","").split(', ')
        surveyObject.Languages = surveyObject.Languages.strip('[]').replace("u'","").replace("'","").split(', ')
        if surveyObject.Languages_Other:
            surveyObject.Languages_Other = surveyObject.Languages_Other.strip('[]').replace("u'","").replace("'","").split(', ')
        surveyObject.CDAD_MemberShip = surveyObject.CDAD_MemberShip.strip('[]').replace("u'","").replace("'","").split(', ')
        surveyObject.CDAD_Services = surveyObject.CDAD_Services.strip('[]').replace("u'","").replace("'","").split(', ')
        return surveyObject
        
    def getContactObject(self):
        """
            get contact objects linked to this location object
        """
        return ContactPanel.objects.filter(Organization_Name__contains=self.Organization_Name)

    def getMeetingObject(self):
        """
            get meeting objects linked to this location object
        """
        return MeetingPanel.objects.filter(Organization_Name__contains=self.Organization_Name)


