import pickle
import json
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/gmail']


def authenticate_gmail():
    creds = None
    if os.path.exists('Api_token/token_gmail.pickle'):
        with open('Api_token/token_gmail.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('Api_token/token_gmail.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    return service


def get_unread_msg(service):
    results = service.users().messages().list(
        userId='me', labelIds=['UNREAD', 'INBOX']).execute()
    messages = results.get('messages', [])

    return messages
