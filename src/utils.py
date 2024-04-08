from model import Email
from database import add_to_db


def mark_email_as_read(client, email: Email):
    #Add the READ label to this email
    #Marking an email as read = Removing the UNREAD label from it
    client.modify_email_labels(email.idField, [], ['UNREAD'])

def mark_email_as_unread(client, email: Email):
    #Add the READ label to this email
    #Marking an email as read = Removing the UNREAD label from it
    client.modify_email_labels(email.idField, ['UNREAD'], [])

def move_message(client, email: Email):
    #Move the email to the destination specified by label argument
    client.modify_email_labels(email.idField, ['INBOX'], [])

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