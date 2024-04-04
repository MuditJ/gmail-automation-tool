from model import Rule, Rules, CollectionPredicate
from typing import List

class RulesExecutor():
    '''An instance of this class takes a rules instance and applies it to a collection of emails'''
    def __init__(self, rules_instance: Rules):
        self.rules_instance = rules_instance

    def get_filtered_emails(self, emails):
        return [email for email in emails if self._check_email(email)]

    def execute_actions_on_filtered_mails(self, emails):
        '''For now, write to a file the action to be performed for each of the filtered emails'''
        pass

    def _check_email(self,email: str) -> bool:
        #Use pattern matching to decide flow?
        if self.rules_instance.collectionPredicate == CollectionPredicate.Any:
            return any(self._check_rule_for_email(rule, email) for rule in self.rules_instance.rules)
        else:
            return all(self._check_rule_for_email(rule, email) for rule in self.rules_instance.rules)
    
    def _check_rule_for_email(self,rule: Rule, email) -> bool:
        '''Check if rule applies for email'''
        pass