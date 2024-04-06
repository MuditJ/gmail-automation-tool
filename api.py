import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_oauth_credentials() -> Credentials:
  """Get OAuth access and refresh token using the client id and secret 
    stored in token.json
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())
    return creds

def call_gmail_api(creds: Credentials) -> List[dict]:
  '''Returns a list of emails'''
  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)
    print("***")
    print(type(service)) #googleapiclient.discovery.Resource
    print(dir(service))
    print('+++++++++++++++++++++++++++++++++++++++++++++++')
    print(type(service.users())) #Also of type googleapiclient.discovery.Resourc
    results = service.users().labels().list(userId="me").execute()
    print(type(results))
    print(results)
    
    labels = results.get("labels", [])

    if not labels:
      print("No labels found.")
      return
    print("Labels:")
    for label in labels:
      print(label["name"])
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print('Getting some emails')
    emails = service.users().messages().list(userId="me", q = '', labelIds=['TRASH']).execute()['messages']
    print(emails)
    for email in emails:
      #Get content of the actual email:
      mail_content: dict = service.users().messages().get(userId = 'me', id = email['id']).execute()
      print(mail_content)
      print('---------------')

  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")

