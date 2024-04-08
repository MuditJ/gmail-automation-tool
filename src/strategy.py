from abc import ABC, abstractmethod
from model import Email, Rule, Field
from datetime import datetime, timedelta, timezone
import re

class PredicateStrategy(ABC):
    '''This is the abstract base class which is used to inherit from for other strategy classes
    which make use of a date based predicate in the rules'''
    format_str = "%a, %d %b %Y %H:%M:%S %z"

    @abstractmethod
    def apply_rule(self, email: Email, rule: Rule):
        pass
    
    def get_email_field_value(self, email: Email, rule: Rule) -> str:
        '''Using the field attribute from the Rule object, get the required email field value'''
        if type(rule.fieldName == Field.contentField):
            return email.contentField
        if type(rule.fieldName == Field.subjectField):
            return email.subjectField
        if type(rule.fieldName == Field.fromField):
            return email.fromField
        if type(rule.fieldName == Field.toField):
            return email.toField
        if type(rule.fieldName == Field.dateReceivedField):
            return email.dateReceivedField
    

    def parse_time_string(self, rule: Rule):
        # Regular expression to extract the quantity and unit of time
        match = re.match(r'(\d+)\s+(\w+)\s+old', rule.value)
        if match:
            quantity = int(match.group(1))
            unit = match.group(2)
            
            # Calculate timedelta based on the unit
            if unit == 'days':
                delta = timedelta(days=quantity)
            elif unit == 'hours':
                delta = timedelta(hours=quantity)
            elif unit == 'months':
                # Estimate the number of days in the past month
                current_date = datetime.now()
                month = current_date.month - quantity
                year = current_date.year
                if month <= 0:
                    year -= 1
                    month += 12
                days_in_month = (current_date.replace(year=year, month=month, day=1) - timedelta(days=1)).day
                delta = timedelta(days=days_in_month)
            elif unit == 'years':
                # Estimate the number of days in the past year
                current_date = datetime.now()
                year = current_date.year - quantity
                days_in_year = (current_date.replace(year=year, month=1, day=1) - timedelta(days=1)).day
                delta = timedelta(days=days_in_year)
            else:
                raise ValueError("Invalid unit of time")

            # Subtract the timedelta from the current datetime
            return datetime.now() - delta
        else:
            raise ValueError("Invalid time string format")
        
    def get_datetime_from_email(self, email:Email):
        return datetime.strptime(email.dateReceivedField, self.format_str)
        


class LessThanPredicateStrategy(PredicateStrategy):
    def apply_rule(self, email: Email, rule: Rule) -> bool:
        email_datetime = self.get_datetime_from_email(email).replace(tzinfo=timezone.utc)
        rule_datetime = self.parse_time_string(rule).replace(tzinfo=timezone.utc)
        print('Email datetime:',email_datetime.strftime("%A, %d %B %Y %H:%M:%S"))
        print('Rule datetime:', rule_datetime.strftime("%A, %d %B %Y %H:%M:%S"))
        print('Checking if email datetime is greater than rule datetime')
        res = email_datetime > rule_datetime
        print('Result: ', res)
        return res



class GreaterThanPredicateStrategy(PredicateStrategy):
    def apply_rule(self, email: Email, rule: Rule):
        email_datetime = self.get_datetime_from_email(email).replace(tzinfo=timezone.utc)
        rule_datetime = self.parse_time_string(rule).replace(tzinfo=timezone.utc)
        print('Email datetime: ', email_datetime.strftime("%A, %d %B %Y %H:%M:%S"))
        print('Rule datetime: ', rule_datetime.strftime("%A, %d %B %Y %H:%M:%S"))
        print('Checking if email datetime is less than rule datetime')
        res = email_datetime < rule_datetime
        print('Result: ', res)
        return res
