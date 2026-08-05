# 清理变量
# region header
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
    sys.path.extend([env])

env = "C:\\Users\\LEEL\\Desktop\\UEGameDesign\\PythonEnv\\"
if env not in sys.path:
    print("Adding new env to sys.path: ", env)
    sys.path.extend([env])

import unreal

print("Unreal Engine Python Environment Initialized.")

from dsl.schema.validator import Validator
from dsl.parser.object_parser import ObjectParser
from dsl.builder.blueprint_builder import BlueprintBuilder
from dsl.builder.ue_reflection import get_nested_property
# endregion


if __name__ == "__main__":
    # a = unreal.load_object(None,"/Game/Game/Core/Veichles/BP_VeichlePawnBase.BP_VeichlePawnBase_C")
    # print(a)
    # from dsl.builder.ue_reflection import get_unreal_class
    # b = get_unreal_class("/Game/Game/Core/Veichles/BP_VeichlePawnBase")
    # print(b)

    yaml_path = r"C:\Users\LEEL\Desktop\UEGameDesign\Data\TestVehicle.yml"
    schema_path = r"C:\Users\LEEL\Desktop\UEGameDesign\Data\scheme.json"
    asset_path = r"/Game/Game/Vehicles/TestVehicle/"

    # Validator
    validator = Validator(schema_path)
    yaml_data = validator.load_yaml(yaml_path)

    if not validator.validate(yaml_data):
        print("YAML 数据校验失败，停止构建。")
        exit()

    # Parser
    parser = ObjectParser()
    builder = BlueprintBuilder()

    for yaml_obj in yaml_data:
        actor_model = parser.parse(yaml_obj)
        # print(actor_model.model_dump_json(indent=4, ensure_ascii=False,serialize_as_any=True))

        blueprint, asset_file_dir = builder.create_blueprint_from_model(
            actor_model, asset_path, overwrite=False
        )
        print(f"Blueprint '{blueprint.get_name()}' 构建完成。")

        # Print all components
        # bp_asset= unreal.load_object(None, asset_path)

        # builder.comp_builder.print_components_info(bp_asset)
        # _ , move_comp = builder.comp_builder.get_component(bp_asset,"VehicleMovementComponent")
        # prop = get_nested_property(move_comp,"EngineSetup.TorqueCurve.ExternalCurve")
        # print(prop)
        # print(type(prop))

    
        # num = builder.comp_builder.delete_all_components(bp_asset)
        # print(f"Successfully Delete {num} comps.")

        builder.tweak_blueprint_from_model(actor_model, asset_file_dir)
        print(f"Blueprint '{asset_path}' 调整完成。")
