import unreal
import sys 
import os
env = "C:\\Users\\LEEL\\Desktop\\UEGameDesign\\PythonEnv\\.venv\\Lib\\site-packages"
if env not in sys.path:
    print("Adding new env to sys.path: ", env)
    sys.path.extend([ env])

import json
import yaml
from jsonschema import validate, ValidationError

def load_schema(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def validate_yaml(yaml_data, schema):
    try:
        validate(instance=yaml_data, schema=schema)
        print("YAML 校验成功！")
    except ValidationError as e:
        print("YAML 校验失败：")
        print(e.message)

if __name__ == "__main__":
    schema_path = r"C:\Users\LEEL\Desktop\UEGameDesign\Python\scheme.json"
    data_path = r"C:\Users\LEEL\Desktop\UEGameDesign\Python\Data\Mini_Tank.yml"

    schema = load_schema(schema_path)
    data = load_yaml(data_path)
    validate_yaml(data, schema)
