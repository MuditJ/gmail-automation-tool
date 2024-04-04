
from model import Rule, Rules, CollectionPredicate, Predicate, Email
from typing import List

class RulesExecutor():
    '''An instance of this class takes a rules instance and applies it to a collection of emails'''
    def __init__(self, rules_instance: Rules):
        self.rules_instance = rules_instance
        

    def _get_filtered_emails(self, emails: List[Email]):
        return [email for email in emails if self._check_email(email)]

    def execute_actions(self, emails: List[Email]):
        '''For now, write to a file the action to be performed for each of the filtered emails'''
        filtered_emails = self._get_filtered_emails(emails)
        #The same actions have to be applied on each email
        #print the list of filtered emals
        print('Filtered emails are:')
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        for email in filtered_emails:
            print(email)
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++')

    def _check_email(self,email: Email) -> bool:
        #Use pattern matching to decide flow?
        if self.rules_instance.collectionPredicate == CollectionPredicate.Any:
            return any(self._check_rule_for_email(rule, email) for rule in self.rules_instance.rules)
        else:
            return all(self._check_rule_for_email(rule, email) for rule in self.rules_instance.rules)
    
    def _check_rule_for_email(self,rule: Rule, email: Email) -> bool:
        '''Check if rule applies for email'''
        email_field_value = RulesExecutor.get_email_field_value(rule.fieldName.value, email)
        print(rule.value, email_field_value)
        if rule.predicate == Predicate.contains:
            contains_func = lambda x,y: x in y 
            return contains_func(rule.value, email_field_value)
        elif rule.predicate == Predicate.not_equal_to:
            not_equal_to_func = lambda x,y: x != y 
            return not_equal_to_func(rule.value, email_field_value)
        elif rule.predicate == Predicate.equal_to:
            equal_to_func = lambda x,y: x == y
            return equal_to_func(rule.value, email_field_value)

    @staticmethod
    def get_email_field_value(fieldName: str, email:Email) -> str:
        if fieldName == "From":
            return email.fromField 
        elif fieldName == "To":
            return email.toField
        elif fieldName == "Date Received":
            return email.dateReceivedField
