import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = [
  'https://www.googleapis.com/auth/drive', # unrestricted access
  'https://www.googleapis.com/auth/drive.file', # per-file access
  'https://www.googleapis.com/auth/drive.readonly', # read-only access
  'https://www.googleapis.com/auth/drive.metadata', # view and manage metadata
  'https://www.googleapis.com/auth/drive.metadata.readonly', # view metadata (read-only)
  'https://www.googleapis.com/auth/drive.appdata', # view and manage its own configuration data
]


def get_drive_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)


def isLoggedIn():
    try:
        if not os.path.exists('token.json'):
            return False
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if creds and creds.valid:
            return True
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            return True
        return False
    except:
        return False
