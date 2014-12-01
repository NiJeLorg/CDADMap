from django.db import models

# Create your models here.

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
        return self.Name
        

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
        return self.Name

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

    class Meta:
        db_table = 'locationPanel'

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
        
class SurveyPanel(models.Model):
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
        
    class Meta:
        db_table = 'surveyPanel'

    def __str__(self):
        return self.Organization_Name
