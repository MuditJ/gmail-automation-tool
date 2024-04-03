import json 
from jsonschema import validate

class RulesJsonValidator():
    ''' Validates the passed json with a json schema'''
    def __init__(self, json_schema = None):
        if not json_schema:
            self.schema = self._load_json_schema()
        else:
            self.schema = json_schema 

    def _load_json_schema(self):
        with open('schema.json', 'r') as f:
            return json.load(f)
        
    def validate_json(self, json_obj):
        res = validate(json_obj, self.schema)
        return res





