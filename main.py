import json

from validator import RulesJsonValidator
from model import Rule,Rules, CollectionPredicate

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
            print(rules_instance)
            print(type(rules_instance))
            print(rules_instance.collectionPredicate == CollectionPredicate.Any)
            print(rules_instance.collectionPredicate == CollectionPredicate.All)
            print(rules_instance.collectionPredicate)
            print(rules_instance.rules)
            #executor = RulesExecutor(rules_instance)
        

if __name__ == "__main__":
    main()