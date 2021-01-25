import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from os.path import expanduser
import requests
import google.auth

home = expanduser("~")
global filepath
filepath = os.path.join(home, '.canvasCal')
client_id = "856179958454-gsehral8n10usv85q9qk4hf5k7mboqlo.apps.googleusercontent.com"
client_secret = "433N07pZ6qjHU45mF8vbFr8p"

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

service = None
creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
def createPickle():
    global service
    # If there are no (valid) credentials available, let the user log in.
    credConfig = {"installed":{"client_id":client_id, "project_id":"canvascal-1608517477785", "auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":client_secret,"redirect_uris":["urn:ietf:wg:oauth:2.0:oob","http://localhost"]}}
    # flow = InstalledAppFlow.from_client_secrets_file(
    #     'credentials.json', SCOPES)
    flow = InstalledAppFlow.from_client_config(credConfig, SCOPES)
    creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open(os.path.join(filepath, 'token.pickle'), 'wb') as token:
        pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)


def loadPickle():
    global service
    if os.path.exists(os.path.join(filepath, 'token.pickle')):
        with open(os.path.join(filepath, 'token.pickle'), 'rb') as token:
            creds = pickle.load(token)
        if not creds or not creds.valid:   
            access_token = refreshToken(client_id, client_secret, creds._refresh_token)
            if access_token:
                creds = google.oauth2.credentials.Credentials(access_token)
            else:
                createPickle()
                return

        service = build('calendar', 'v3', credentials=creds)
    else:
        createPickle()


def refreshToken(client_id, client_secret, refresh_token):
    params = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token
    }

    authorization_url = "https://www.googleapis.com/oauth2/v4/token"
    r = requests.post(authorization_url, data=params)

    if r.ok:
        return r.json()['access_token']
    else:
        return None

def printCalendars():
    global service
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
    global service
    calendar = {
        'summary': 'Canvas Assignments',
        'timeZone': 'UTC'
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
