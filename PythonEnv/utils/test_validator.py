# dsl/main_test.py
from dsl.schema.validator import Validator
from dsl.parser.object_parser import ObjectParser

if __name__ == "__main__":
    schema_path = r"C:\Users\LEEL\Desktop\UEGameDesign\Data\scheme.json"
    data_path = r"C:\Users\LEEL\Desktop\UEGameDesign\Data\Schema_Test.yml"
    
    validator = Validator(schema_path)
    yaml_data = validator.load_yaml(data_path)

    validator.validate(yaml_data)
   
    parser = ObjectParser()
    actor_model = parser.parse(yaml_data)

    # print(actor_model.model_dump())
    print(actor_model.model_dump_json(indent=4, ensure_ascii=False))
    print(actor_model)

