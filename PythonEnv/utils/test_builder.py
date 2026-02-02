# 清理变量
for name in list(globals().keys()):
    if name not in ["__builtins__", "__name__", "__doc__"]:
        del globals()[name]
import sys
# 清理模块缓存
for key in list(sys.modules.keys()):
    if key.startswith("dsl."): 
        del sys.modules[key]


import sys
env = "C:\\Users\\LEEL\\Desktop\\UEGameDesign\\PythonEnv\\.venv\\Lib\\site-packages"
if env not in sys.path:
    print("Adding new env to sys.path: ", env)
    sys.path.extend([ env])

env = "C:\\Users\\LEEL\\Desktop\\UEGameDesign\\PythonEnv\\"
if env not in sys.path:
    print("Adding new env to sys.path: ", env)
    sys.path.extend([ env])

import unreal
print("Unreal Engine Python Environment Initialized.")

from dsl.schema.validator import Validator
from dsl.parser.object_parser import ObjectParser
from dsl.builder.blueprint_builder import BlueprintBuilder

def run_builder_test(yaml_path:str,asset_path:str=r"/Game/Game/Generated/BP_TestActor"):
    schema_path = r"C:\Users\LEEL\Desktop\UEGameDesign\Data\scheme.json"

    validator = Validator(schema_path)
    yaml_data = validator.load_yaml(yaml_path)

    if not validator.validate(yaml_data):
        print("YAML 数据校验失败，停止构建。")
        return

    parser = ObjectParser()
    actor_model = parser.parse(yaml_data)

    builder = BlueprintBuilder()

    # blueprint = builder.create_blueprint_from_model(actor_model, asset_path)
    # print(f"Blueprint '{blueprint.get_name()}' 构建完成。")

    builder.tweak_blueprint_from_model(actor_model, asset_path)
    print(f"Blueprint '{asset_path}' 调整完成。")


if __name__ == "__main__":
    yaml_test_path = r"C:\Users\LEEL\Desktop\UEGameDesign\Data\MiniTank_Test.yml"
    run_builder_test(yaml_test_path)
    

