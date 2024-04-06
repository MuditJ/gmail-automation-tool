import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from database import prepare_db, add_to_db
from typing import List

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def main():
  """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
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

  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)
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
  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")

  print(type(emails))
  print(emails) #This looks like: [{'id': '18ead77b4c049041', 'threadId': '18ead7785dbb69d7'}, {'id': '18ead7709bafac38', 'threadId': '18ead76c7c194571'}]
  data = []
  for email in emails:
    print("////////////////")
    #Get content of the actual email:
    mail_content: dict = service.users().messages().get(userId = 'me', id = email['id']).execute()
    print(mail_content['id'], mail_content['labelIds'], mail_content['snippet'])
    print(mail_content['payload']['headers'][1:6])
    print('---------------')
    prepare_data_and_add_to_db(mail_content)
  return data

def prepare_data_and_add_to_db(mail_content: dict):
  data = {}
  data['Id'] = mail_content['id']
  data['Content'] = mail_content['snippet']
  data['Date'] = mail_content['payload']['headers'][1]['value']
  data['Subject'] = mail_content['payload']['headers'][3]['value']
  data['From'] = mail_content['payload']['headers'][4]['value']
  data['To'] = mail_content['payload']['headers'][5]['value']
  #Add entry to db
  print('Adding entry to db')
  add_to_db('email_database.db', data, 'Email')

if __name__ == "__main__":
  prepare_db()
  main()
