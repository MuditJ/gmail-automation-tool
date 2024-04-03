import json

from validator import RulesJsonValidator

def main():
    validator = RulesJsonValidator()
    with open('rule-samples/another-incorrect-sample.json','r') as json_file:
        json_obj = json.load(json_file)
    validator.validate_json(json_obj)

if __name__ == "__main__":
    main()