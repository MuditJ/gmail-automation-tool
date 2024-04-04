from typing import List
from enum import Enum
from pydantic import BaseModel, Field
'''These represent the different json objects at various levels of nesting that the rules json represent'''


class Email(BaseModel):
    fromField: str 
    toField: str
    dateReceivedField: str
    contentField: str
    subjectField: str

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

class Rule(BaseModel):
    fieldName: Field
    predicate: Predicate
    value: str

class Rules(BaseModel):
    collectionPredicate: CollectionPredicate
    rules: List[Rule]
    actions: List[Action]
