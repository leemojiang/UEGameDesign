import json
import yaml
from jsonschema import validate, ValidationError


class Validator:
    """负责加载 JSON Schema 并校验 YAML 数据"""

    def __init__(self, schema_path: str):
        self.schema_path = schema_path
        self.schema = self._load_schema(schema_path)

    def _load_schema(self, path: str) -> dict:
        """加载 JSON Schema 文件"""
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_yaml(self, path: str) -> list:
        """加载 YAML 文件，支持流式加载多个文档"""
        with open(path, "r", encoding="utf-8") as f:
            return list(yaml.safe_load_all(f))

    def validate(self, yaml_data: list) -> bool:
        """校验 YAML 数据，返回 True/False"""
        try:
            for doc in yaml_data:
                validate(instance=doc, schema=self.schema)
            print("YAML 校验成功！")
            return True
        except ValidationError as e:
            print("YAML 校验失败：")
            print(e.message)
            return False


if __name__ == "__main__":
    schema_path = r"C:\Users\LEEL\Desktop\UEGameDesign\Data\scheme.json"
    data_path = r"C:\Users\LEEL\Desktop\UEGameDesign\Data\Schema_Test.yml"

    validator = Validator(schema_path)
    yaml_data = validator.load_yaml(data_path)
    validator.validate(yaml_data)
