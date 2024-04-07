from abc import ABC, abstractmethod
from model import Email, Rule, Field
import datetime
import re
from datetime import datetime, timedelta
from apiclient import GoogleAPIClient
from typing import List


def mark_email_as_read(client: GoogleAPIClient, email: Email):
    #Add the READ label to this email
    #Marking an email as read = Removing the UNREAD label from it
    client.modify_email_labels(email.idField, [], ['UNREAD'])

def mark_email_as_unread(client: GoogleAPIClient, email: Email):
    #Add the READ label to this email
    #Marking an email as read = Removing the UNREAD label from it
    client.modify_email_labels(email.idField, ['UNREAD'], [])

def move_message(client: GoogleAPIClient, email: Email):
    #Move the email to the destination specified by label argument
    client.modify_email_labels(email.idField, ['INBOX'], [])