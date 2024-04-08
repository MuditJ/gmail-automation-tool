
from model import Rule, Rules, CollectionPredicate, Predicate, Email, Action
from typing import List
from utils import *
from database import update_email_as_filtered
from strategy import GreaterThanPredicateStrategy, LessThanPredicateStrategy

class RulesExecutor():
    '''An instance of this class takes a rules instance and applies it to a collection of emails'''

    action_mapping: dict = {
        Action.mark_as_read: mark_email_as_read,
        Action.mark_as_unread: mark_email_as_unread,
        Action.move_message: move_message
    }

    def __init__(self, rules_instance: Rules, client):
        self.rules_instance = rules_instance
        self.client = client
        

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
            #Update in database and set the FILTERED column as 1
            update_email_as_filtered(email.idField)
            print(email)
            for action in self.rules_instance.actions:
                print('Applying action..')
                print(action.name)
                action_func = self.action_mapping[action]
                #Perform action
                action_func(self.client, email)
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
        if rule.predicate == Predicate.contains:
            contains_func = lambda x,y: x in y 
            return contains_func(rule.value, email_field_value)
        elif rule.predicate == Predicate.not_equal_to:
            not_equal_to_func = lambda x,y: x != y 
            return not_equal_to_func(rule.value, email_field_value)
        elif rule.predicate == Predicate.equal_to:
            equal_to_func = lambda x,y: x == y
            return equal_to_func(rule.value, email_field_value)
        elif rule.predicate == Predicate.greater_than:
            strategy = GreaterThanPredicateStrategy()
            return strategy.apply_rule(email, rule)
        elif rule.predicate == Predicate.less_than:
            strategy = LessThanPredicateStrategy()
            return strategy.apply_rule(email, rule)
        else:
            return False 



    @staticmethod
    def get_email_field_value(fieldName: str, email:Email) -> str:
        if fieldName == "From":
            return email.fromField 
        elif fieldName == "To":
            return email.toField
        elif fieldName == "Date Received":
            return email.dateReceivedField
        elif fieldName == "Subject":
            return email.subjectField
        elif fieldName == "Content":
            return email.contentField
