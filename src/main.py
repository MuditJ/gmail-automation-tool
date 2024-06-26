import json

from validator import RulesJsonValidator
from model import Email,Rules, CollectionPredicate
from typing import List
from executor import RulesExecutor
from database import load_emails_from_db
import os
from apiclient import GoogleAPIClient


def parse_email_file(file_path: str) -> Email:
    with open(file_path, 'r') as file:
        lines = file.readlines()

    email_data = {}
    for line in lines:
        key, value = line.strip().split(':', 1)
        email_data[key] = value 
    

    return Email(**email_data)

def convert_text_files_to_emails(directory: str) -> List[Email]:
    emails = []
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            email = parse_email_file(file_path)
            emails.append(email)
    return emails

def main():
    validator = RulesJsonValidator()
    with open('rule-samples/second-correct-sample.json','r') as json_file:
        json_obj = json.load(json_file)
        try:
            validator.validate_json(json_obj)
        except:
            print('Validation error')
            return
        else:
            print('The JSON is valid')
            print(json_obj)
            #Load the json into a model instance using pydantic
            rules_instance = Rules.model_validate(json_obj)
            #Convert all the emails in email samples into Pydantic model objects
            emails = load_emails_from_db()
            #emails = convert_text_files_to_emails('./email-samples')
            print('*********')
            for email in emails:
                print(email)

            #Create instance of executor to run the emails through
            client = GoogleAPIClient()
            client.get_credentials()
            executor = RulesExecutor(rules_instance, client)
            executor.execute_actions(emails)


if __name__ == "__main__":
    main()