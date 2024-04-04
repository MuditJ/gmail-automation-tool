from dataclasses import dataclass 
from typing import List
from enum import Enum
from pydantic import BaseModel, validator, EmailStr
'''These represent the different json objects at various levels of nesting that the rules json represent'''


class CollectionPredicate(Enum):
    Any: str = "Any"
    All: str = "All"

class Predicate(Enum):
    less_than: str = "less than"
    contains: str = "contains"
    greater_than: str = "greater than"
    equal_to: str = "equal to"
    not_equal_to: str = "not equal to"

class Action(Enum):
    mark_as_read: str = "Mark as read"
    mark_as_unread: str = "Mark as unread"
    move_message: str = "Move message"

class Field(Enum):
    fromField: str = "From"
    toField: str = "To"
    dateReceivedField: str = "Date Received"

@dataclass
class Rule(BaseModel):
    fieldName: Field
    predicate: Predicate
    value: str

'''
    @validator('fieldValue')
    def validate_field_value(cls, v, values, **kwargs):
        if values.get('fieldName') in [Field.fromField, Field.toField]:
            # If fieldName is "From" or "To", validate fieldValue as an email
            if not EmailStr.validate(v):
                raise ValueError(f'Invalid email address for {values["fieldName"]} field')
        return v
'''
@dataclass
class Rules(BaseModel):
    collectionPredicate: CollectionPredicate
    rules: List[Rule]
    actions: List[Action]
