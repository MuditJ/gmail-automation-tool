import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List
from database import add_to_db, prepare_db
from utils import prepare_data_and_add_to_db


class GoogleAPIClient():

  SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

  def __init__(self):
    self.token = self.get_credentials()
    self.service = build("gmail", "v1", credentials=self.token)
    self.labels = None
    self.emails = None

  def get_credentials(self):
    '''Get credentials for authorization with the resource server'''
    creds = None 
    if os.path.exists("token.json"):
      creds = Credentials.from_authorized_user_file("token.json", self.SCOPES)
      return creds
      # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        #Use the client id and secret defined in credentials.json
        #to run OAuth flow
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", self.SCOPES
        )
        creds = flow.run_local_server(port=0)
        print(creds)
      # Save the credentials for the next run
        with open("token.json", "w") as token:
          token.write(creds.to_json())
      return creds

  def fetch_emails(self, labels: List[str] = None):
    emails: dict = self.service.users().messages().list(userId="me", q = '', labelIds=['TRASH']).execute()
    if emails.get('resultSizeEstimate') == 0:
      print('No emails found for currently set filters')
      return []
    else:
      print(emails)
      messages = emails['messages']
      email_messages = []
      for message in messages:
          mail_content: dict = self.service.users().messages().get(userId = 'me', id = message['id']).execute()
          email_messages.append(mail_content)
      return email_messages

  def modify_email_labels(self, emailId, labelsToAdd: List[str] = [], labelsToRemove: List[str] = []):
    '''Modify labels (add and/or remove) for an email'''
    self.service.users().messages().modify(userId='me', id = emailId, body = {'addLabelIds' : labelsToAdd, 'removeLabelIds' : labelsToRemove}).execute()


  def fetch_labels(self):
    '''Fetches all the labels'''
    results = self.service.users().labels().list(userId="me").execute()
    labels = results.get("labels", [])
    return [label['name'] for label in labels]
  

if __name__ == "__main__":
  #prepare_db()
  #Create client class:
  client = GoogleAPIClient()
  client.get_credentials()
  print(client.fetch_labels())
  emails = client.fetch_emails()
  #Prepare DB
  prepare_db()
  for email in emails:
    print(email)
    print('****')
    prepare_data_and_add_to_db(email)
  #Add these emails to DB
  #Move all these fetched emails:
  #email_ids = [email['id'] for email in emails]
  print('Done')