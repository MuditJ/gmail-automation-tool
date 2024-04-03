TASK:
Write a standalone Python script that integrates with Gmail API and performs some rule based operations on emails.

DETAILS:
- Write s standalone Python script and not a full fledged web application. Third party packages can be used
- Authenticate to Google's Gmail API using OAuth and fetch a list of emails from inbox
- Come up with a DB representation and store these emails. Use any relational DB
- Now that you can fetch emails, write another script that can process emails based on some rules and take some actions on them using the Gmail API
- The rules to be used for processing have the following JSON schema:
{
	"field_name": "From/To/Subject/Date Received/",
	"predicate" : "contains/not equal/less than/greater than", 
	"value" :"Some value for the field specified by the field_name"
}

