import sys,os
from django.core.management.base import BaseCommand, CommandError
from cdadmap.models import Contact, ContactPanel, Location, LocationPanel, Meeting, MeetingPanel, Survey, SurveyPanel
import csv


"""
  Loads original CDAD data from CSV
"""
class Command(BaseCommand):
    
    def load_data(self):
        """

        """
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        # open contact.csv and dump into Contact table
        with open(os.path.join(__location__, 'contact.csv'), 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] != 'id': # Ignore the header row, import everything else
                    contact = Contact()
                    contact.id = row[0]
                    contact.Organization_Name = row[1]
                    contact.Name = row[2]
                    contact.Title = row[3]
                    contact.Tel = row[4]
                    contact.Email = row[5]
                    contact.KeepPrivate = row[6]
                    contact.AddListPermission = row[7]
                    contact.MyTrace = row[8]
                    contact.save()

        # open contact.csv and dump into ContactPanel table
        with open(os.path.join(__location__, 'contact.csv'), 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] != 'id': # Ignore the header row, import everything else
                    contactpanel = ContactPanel()
                    contactpanel.id = row[0]
                    contactpanel.Organization_Name = row[1]
                    contactpanel.Name = row[2]
                    contactpanel.Title = row[3]
                    contactpanel.Tel = row[4]
                    contactpanel.Email = row[5]
                    contactpanel.KeepPrivate = row[6]
                    contactpanel.AddListPermission = row[7]
                    contactpanel.save()

        # open location.csv and dump into Location table
        with open(os.path.join(__location__, 'location.csv'), 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] != 'id': # Ignore the header row, import everything else
                    location = Location()
                    location.id = row[0]
                    location.Organization_Name = row[1]
                    location.Address = row[2]
                    location.Address2 = row[3]
                    location.City = row[4]
                    location.ZipCode = row[5]
                    location.State = row[6]
                    location.MailingAddress = row[7]
                    location.KeepPrivate = row[8]
                    location.Activity = row[9]
                    location.MyTrace = row[10]
                    location.save()
                
        # open location.csv and dump into LocationPanel table
        with open(os.path.join(__location__, 'location.csv'), 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] != 'id': # Ignore the header row, import everything else
                    locationpanel = LocationPanel()
                    locationpanel.idlocation = row[0]
                    locationpanel.Organization_Name = row[1]
                    locationpanel.Address = row[2]
                    locationpanel.Address2 = row[3]
                    locationpanel.City = row[4]
                    locationpanel.ZipCode = row[5]
                    locationpanel.State = row[6]
                    locationpanel.MailingAddress = row[7]
                    locationpanel.KeepPrivate = row[8]
                    locationpanel.Activity = row[9]
                    locationpanel.save()

        # open meeting.csv and dump into Meeting table
        with open(os.path.join(__location__, 'meeting.csv'), 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] != 'id': # Ignore the header row, import everything else
                    meeting = Meeting()
                    meeting.id = row[0]
                    meeting.Organization_Name = row[1]
                    meeting.hasMeeting = row[2]
                    meeting.MeetingName = row[3]
                    meeting.Address = row[4]
                    meeting.Address2 = row[5]
                    meeting.City = row[6]
                    meeting.ZipCode = row[7]
                    meeting.State = row[8]
                    meeting.Repeat1 = row[9]
                    meeting.RepeatEvery = row[10]
                    meeting.Time1 = row[11]
                    meeting.StartOn = row[12]
                    meeting.EndsOn = row[13]
                    meeting.Occurances = row[14]
                    meeting.On1 = row[15]
                    meeting.MeetingPerson = row[16]
                    meeting.MeetingPersonPhone = row[17]
                    meeting.MeetingPersonEmail = row[18]
                    meeting.MeetAlways = row[19]
                    meeting.MyTrace = row[20]
                    meeting.save()
                
        # open meeting.csv and dump into MeetingPanel table
        with open(os.path.join(__location__, 'meeting.csv'), 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] != 'id': # Ignore the header row, import everything else
                    meetingpanel = MeetingPanel()
                    meetingpanel.id = row[0]
                    meetingpanel.Organization_Name = row[1]
                    meetingpanel.hasMeeting = row[2]
                    meetingpanel.MeetingName = row[3]
                    meetingpanel.Address = row[4]
                    meetingpanel.Address2 = row[5]
                    meetingpanel.City = row[6]
                    meetingpanel.ZipCode = row[7]
                    meetingpanel.State = row[8]
                    meetingpanel.Repeat1 = row[9]
                    meetingpanel.RepeatEvery = row[10]
                    meetingpanel.Time1 = row[11]
                    meetingpanel.StartOn = row[12]
                    meetingpanel.EndsOn = row[13]
                    meetingpanel.Occurances = row[14]
                    meetingpanel.On1 = row[15]
                    meetingpanel.MeetingPerson = row[16]
                    meetingpanel.MeetingPersonPhone = row[17]
                    meetingpanel.MeetingPersonEmail = row[18]
                    meetingpanel.MeetAlways = row[19]
                    meetingpanel.save()                

        # open survey.csv and dump into Survey table
        with open(os.path.join(__location__, 'survey.csv'), 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] != 'id': # Ignore the header row, import everything else
                    survey = Survey()
                    survey.id = row[0]
                    survey.Organization_Name = row[1]
                    survey.Organizaton_Acronym = row[2]
                    survey.Survey_Taker_Name = row[3]
                    survey.Survey_Taker_Email_Address = row[4]
                    survey.Survey_Taker_Email_AddToList = row[5]
                    survey.Organization_Description = row[6]
                    survey.Year_Founded = row[7]
                    survey.Organization_Logo = row[8]
                    survey.Organizational_Mission = row[9]
                    survey.Social_Email = row[10]
                    survey.AddSocial_Email = row[11]
                    survey.Social_facebook = row[12]
                    survey.Social_website = row[13]
                    survey.Social_Twitter = row[14]
                    survey.Social_other_media = row[15]
                    survey.Service_Area_Description = row[16]
                    survey.Service_Area_Geographic_Boundaries = row[17]
                    survey.MapDissolve = row[18]
                    survey.organization_structured = row[19]
                    survey.governance_board = row[20]
                    survey.No_of_board_members = row[21]
                    survey.staff_members = row[22]
                    survey.Activities_Services = row[23]
                    survey.Service_Population = row[24]
                    survey.Languages = row[25]
                    survey.accomplish_one_title = row[26]
                    survey.accomplish_one_description = row[27]
                    survey.accomplish_two_title = row[28]
                    survey.accomplish_two_description = row[29]
                    survey.accomplish_three_title = row[30]
                    survey.accomplish_three_description = row[31]
                    survey.accomplish_four_title = row[32]
                    survey.accomplish_four_description = row[33]
                    survey.accomplish_five_title = row[34]
                    survey.accomplish_five_description = row[35]
                    survey.Partnerships_Networks = row[36]
                    survey.CDAD_MemberShip = row[37]
                    survey.CDAD_Services = row[38]
                    survey.CDAD_Comments = row[39]
                    survey.CDAD_FeedBack = row[40]
                    survey.MyTrace = row[41]
                    survey.save()
                
        # open survey.csv and dump into SurveyPanel table
        with open(os.path.join(__location__, 'survey.csv'), 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] != 'id': # Ignore the header row, import everything else
                    surveypanel = SurveyPanel()
                    surveypanel.id = row[0]
                    surveypanel.Organization_Name = row[1]
                    surveypanel.Organizaton_Acronym = row[2]
                    surveypanel.Survey_Taker_Name = row[3]
                    surveypanel.Survey_Taker_Email_Address = row[4]
                    surveypanel.Survey_Taker_Email_AddToList = row[5]
                    surveypanel.Organization_Description = row[6]
                    surveypanel.Year_Founded = row[7]
                    surveypanel.Organization_Logo = row[8]
                    surveypanel.Organizational_Mission = row[9]
                    surveypanel.Social_Email = row[10]
                    surveypanel.AddSocial_Email = row[11]
                    surveypanel.Social_facebook = row[12]
                    surveypanel.Social_website = row[13]
                    surveypanel.Social_Twitter = row[14]
                    surveypanel.Social_other_media = row[15]
                    surveypanel.Service_Area_Description = row[16]
                    surveypanel.Service_Area_Geographic_Boundaries = row[17]
                    surveypanel.MapDissolve = row[18]
                    surveypanel.organization_structured = row[19]
                    surveypanel.governance_board = row[20]
                    surveypanel.No_of_board_members = row[21]
                    surveypanel.staff_members = row[22]
                    surveypanel.Activities_Services = row[23]
                    surveypanel.Service_Population = row[24]
                    surveypanel.Languages = row[25]
                    surveypanel.accomplish_one_title = row[26]
                    surveypanel.accomplish_one_description = row[27]
                    surveypanel.accomplish_two_title = row[28]
                    surveypanel.accomplish_two_description = row[29]
                    surveypanel.accomplish_three_title = row[30]
                    surveypanel.accomplish_three_description = row[31]
                    surveypanel.accomplish_four_title = row[32]
                    surveypanel.accomplish_four_description = row[33]
                    surveypanel.accomplish_five_title = row[34]
                    surveypanel.accomplish_five_description = row[35]
                    surveypanel.Partnerships_Networks = row[36]
                    surveypanel.CDAD_MemberShip = row[37]
                    surveypanel.CDAD_Services = row[38]
                    surveypanel.CDAD_Comments = row[39]
                    surveypanel.CDAD_FeedBack = row[40]
                    surveypanel.save()

    def handle(self, *args, **options):
        print "Loading Data...."
        self.load_data()





