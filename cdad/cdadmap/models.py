from django.db import models

# CDAD models below
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

# SurveyPanel defined first to allow foreign key relationship to come late        
class SurveyPanel(models.Model):
    id = models.IntegerField(null=False, primary_key=True)
    Organization_Name = models.TextField(unique=True)
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
        
    class Meta:
        db_table = 'surveyPanel'

    def __str__(self):
        return self.Organization_Name

    def Organization_Description_as_list(self):
        Organization_Descriptions = self.Organization_Description.replace(', ','| ')
        Organization_Descriptions = Organization_Descriptions.split(',')
        for Organization_Description in Organization_Descriptions:
            Organization_Description.replace('|', ',')
        return Organization_Descriptions

    def Service_Area_Description_as_list(self):
        Service_Area_Descriptions = self.Service_Area_Description.replace(', ','| ')
        Service_Area_Descriptions = Service_Area_Descriptions.split(',')
        for Service_Area_Description in Service_Area_Descriptions:
            Service_Area_Description.replace('|', ',')
        return Service_Area_Descriptions

    def organization_structured_as_list(self):
        organization_structureds = self.organization_structured.replace(', ','| ')
        organization_structureds = organization_structureds.split(',')
        for organization_structured in organization_structureds:
            organization_structured.replace('|', ',')
        return organization_structureds

    def Activities_Services_as_list(self):
        Activities_Servicess = self.Activities_Services.replace(', ','| ')
        Activities_Servicess = Activities_Servicess.split(',')
        for Activities_Services in Activities_Servicess:
            Activities_Services = Activities_Services.replace("|", ",")
        return Activities_Servicess

    def Service_Population_as_list(self):
        Service_Populations = self.Service_Population.replace(', ','| ')
        Service_Populations = Service_Populations.split(',')
        for Service_Population in Service_Populations:
            Service_Population.replace('|', ',')
        return Service_Populations

    def Languages_as_list(self):
        Languagess = self.Languages.replace(', ','| ')
        Languagess = Languagess.split(',')
        for Languages in Languagess:
            Languages.replace('|', ',')
        return Languagess


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
    KeepPrivate = models.TextField()
    AddListPermission = models.TextField()
    
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

class MeetingPanel(models.Model):
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

    class Meta:
        db_table = 'meetingpanel'

    def __str__(self):
        return self.Organization_Name


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
    MailingAddress = models.TextField()
    KeepPrivate = models.TextField()
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
        return SurveyPanel.objects.get(Organization_Name=self.Organization_Name_SurveyPanel_FK)
        
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

    def Activity_as_list(self):
        activities = self.Activity.replace(', ','| ')
        activities = activities.split(',')
        for activity in activities:
            activity.replace('| ', ', ')
        return activities
