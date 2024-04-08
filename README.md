## gmail automation tool

This is a CLI application which automates the task of filtering emails in your inbox and applying different operations (like Mark as read/unread, Move to inbox/spam) for you. 
It uses OAuth to authenticate with the Gmail API.


### Installation

- Create a Python virtual environment and install the dependencies (below steps are for Mac and Linux)
```
python3 -m venv env
source venv/bin/activate
pip install requirements.txt
```
* On windows, the command to activate the created virtual environment is:

Optionally, you can also install DB Browser for Sqlite to view the stored data (fetched emails, filtered emails etc) in a more convenient way. 

### Running the application

- There are two aspects to running this application: 

    i. Authenticating with Google OAuth server, fetching the emails from Gmail API and preparing the database tables

    ii. Running the rules.json against the fetched emails

    - For the first step, run apiclient.py directly as a script:

    `python3 apiclient.py`

    This will:

        . Create the access and refresh token to be used when making requests to the Gmail API

        . Create the database and tables

        . Fetch emails from the Gmail API


- For the second step, you can either update a sample rules.json or use the existing 'second-correct-samples.json'. The rules.json should be placed inside /rule-samples and obey the schema defined by schema.json

    To run this:
    
    `python3 main.py`

    This will:
       
        . Fetch the stored emails in the database
       
        . Validate the rules.json passed to see if it obeys the json schema defined in schema.json
       
        . Apply the rules against the emails, filter out the ones which are valid, and perform the mentioned actions

