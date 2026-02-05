from dsl.schema.validator import Validator
from dsl.parser.object_parser import ObjectParser

if __name__ == "__main__":
    # import pydantic 
    # print(pydantic.VERSION)

    yaml_path = r"C:\Users\Administrator\Desktop\ARcDesign\Data\MiniTank_Test.yml"
    schema_path = r"C:\Users\Administrator\Desktop\ARcDesign\Data\scheme.json"
    asset_path=r"/Game/Game/Generated/BP_TestActor"

    # Validator
    validator = Validator(schema_path)
    yaml_data = validator.load_yaml(yaml_path)

    if not validator.validate(yaml_data):
        print("YAML 数据校验失败，停止构建。")
        exit()

    parser = ObjectParser()

    for yaml_obj in yaml_data:
        actor_model =parser.parse(yaml_obj)
        print(actor_model.model_dump_json(indent=4,ensure_ascii=True,serialize_as_any=True,exclude_none=True))
        print(actor_model)
