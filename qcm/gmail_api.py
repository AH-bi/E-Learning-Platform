# gmail_api.py
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from base64 import urlsafe_b64encode, urlsafe_b64decode
from email.mime.text import MIMEText
import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials

def load_client_id():
    with open('/home/ab/Desktop/client_secret.json') as f:
        client_id = json.load(f)
        print(client_id)
    return client_id

creds = Credentials.from_authorized_user_info(info=load_client_id())

def send_verification_email(to, subject, body):
    try:
        service = build('gmail', 'v1', credentials=creds)
        message = create_message(to, subject, body)
        send_message(service, "me", message)
        print("Email sent!")
    except HttpError as error:
        print("An error occurred: %s" % error)

def create_message(to, subject, body):
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}


def send_message(service, user_id, message, to):
    try:
        message = (service.users().messages().send(user_id=user_id, body=message).execute())
        print(F'Email was sent to {to} with Message Id: {message["id"]}')
    except HttpError as error:
        print(F'An error occurred: {error}')
