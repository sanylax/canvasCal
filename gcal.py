from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        credConfig = {"installed":{"client_id":"806245814001-v03kkhur6vm9asi8q9gblgtef52552su.apps.googleusercontent.com","project_id":"canvas-1608438105562","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"gWnHi74RqUDtHffznIxfCLGs","redirect_uris":["urn:ietf:wg:oauth:2.0:oob","http://localhost"]}}
        # flow = InstalledAppFlow.from_client_secrets_file(
        #     'credentials.json', SCOPES)
        flow = InstalledAppFlow.from_client_config(credConfig, SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('calendar', 'v3', credentials=creds)

def printCalendars():
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            print(calendar_list_entry['summary']) 
            print(calendar_list_entry['id'])

        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

def createCalendar():
    calendar = {
        'summary': 'Canvas Assignments 2.0',
        'timeZone': 'America/Los_Angeles'
    }
    created_calendar = service.calendars().insert(body=calendar).execute()
    ourCalendarId = created_calendar['id']
    print(ourCalendarId)
    print(created_calendar['summary'])
    return ourCalendarId
    
    

def addEvent(assignmentID, assignmentName, assignmentTime, assignmentDescription, calendar):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    event = {
        'id': assignmentID,
        'summary': assignmentName,
        'description': assignmentDescription,
        'start': {
            'dateTime': assignmentTime,
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': assignmentTime,
            'timeZone': 'UTC',
        },
        
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 60},
            ],
        },
    }
    event = service.events().insert(calendarId = calendar, body=event).execute()
    #print(event)
    #print(event['eventId'])

def editEvent(assignmentID, assignmentName, assignmentTime, assignmentDescription, calendar):
    print("edit event")
    event = {
        'id': assignmentID,
        'summary': assignmentName,
        'description': assignmentDescription,
        'start': {
            'dateTime': assignmentTime,
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': assignmentTime,
            'timeZone': 'UTC',
        },
        
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 60},
            ],
        },
    }
    event = service.events().update(calendarId=calendar, body=event, eventId = str(assignmentID)).execute()
    
    # """Shows basic usage of the Google Calendar API.
    # Prints the start and name of the next 10 events on the user's calendar.
    # """    
    # #now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    # now = datetime.datetime.utcnow().replace(day=1) - datetime.timedelta(days=1)
    # now = now.isoformat() + 'Z'
    # events_result = service.events().list(calendarId='primary', timeMin=now,
    #                                     maxResults=50, singleEvents=True,
    #                                     orderBy='startTime').execute()
    # events = events_result.get('items', [])
    # if not events:
    #     return -2
    # print(type(assignmentID))
    # for event in events:
    #     #print(event['description'])
    #     print(event.get('description'))
    #     print(type(event.get('description')))
    #     if str(assignmentID) == event.get('description'):
    #         service.events().delete(calendarId='primary', eventId=event.get).execute()


    #         return 0
    
    # return -1


    '''
    event = {
        'summary': assignmentName,
        'location': '800 Howard St., San Francisco, CA 94103',
        'description': assignmentID,
        'start': {
            'dateTime': assignmentTime,
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': assignmentTime,
            'timeZone': 'UTC',
        },
        
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 60},
            ],
        },
    }
    event = service.events().insert(calendarId='primary', body=event).execute()

    #events.insert()
    '''

# main('test assignment', '456', 10)