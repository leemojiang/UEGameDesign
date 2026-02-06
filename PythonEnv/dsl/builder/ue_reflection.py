# dsl/builder/ue_reflection.py
import unreal
from pydantic import BaseModel

def get_nested_property(obj,path):
    parts = path.split(".")
    target = obj

    for p in parts:
        target = target.get_editor_property(p)
    
    return target

def set_nested_property(obj, path, value):
    # set_nested_property(movement, "EngineSetup.MaxRPM", 8000)
    parts = path.split(".")
    target = obj

    for p in parts[:-1]:
        target = target.get_editor_property(p)

    target.set_editor_property(parts[-1], value)
    
def apply_properties(obj, props: dict , ignore_keys = []):
    # movement = cdo.get_component_by_class(unreal.ChaosWheeledVehicleMovementComponent)
    # engine = {"EngineSetup":{"MaxRPM":8000}}
    # apply_properties(movement,engine)
    for key, value in props.items():
        try:
            obj.get_editor_property(key)
        except:
            unreal.log_warning(f"[属性不存在] {obj} 没有属性 {key}")
            continue

        if isinstance(value, dict):
            sub = obj.get_editor_property(key)
            apply_properties(sub, value)
            obj.set_editor_property(key, sub)
        else:  
            try:
                obj.set_editor_property(key, value)
                print(f"Set {key} : {value} for {obj}")
            except Exception as e:
                unreal.log_warning(f"[Actor属性失败] {key}={value}, 错误: {e}")

def apply_basemodel_properties(obj,props_model:BaseModel,ignore_keys=[]):
    # props = props_model.model_dump(exclude_none=True)
    for key,value in props_model.__dict__.items():
        if value is None or key in ignore_keys:
            continue

        try:
            ue_value = obj.get_editor_property(key)
        except:
            print(f"[属性不存在] {obj} 没有属性 {key}")
            continue

        # ------------------------- # BaseModel → 递归 # ------------------------- 
        if isinstance(value, BaseModel): 
            apply_basemodel_properties(ue_value, value) 
            obj.set_editor_property(key, ue_value) 
            continue

        # ------------------------- # dict → 直接整体写入（TMap） # ------------------------- 
        elif isinstance(value, dict): 
            if ue_value.__class__.__name__ == "RuntimeFloatCurve": 
                

                obj.set_editor_property(key, ue_value) 
                print(f"Set RuntimeFloatCurve {key} = {value}") 
                continue

            obj.set_editor_property(key, value) 
            print(f"Set dict {key} = {value}") 
            continue
        
        # List 数组处理
        elif isinstance(value, list):
            new_list = []
            for item in value:
                if isinstance(item, BaseModel):
                    # 创建 struct 实例
                    try:
                        struct_item = ue_value[0].__class__() if len(ue_value) > 0 else None
                    except Exception:
                        struct_item = None

                    if struct_item:
                        apply_basemodel_properties(struct_item, item)
                        new_list.append(struct_item)
                    else:
                        new_list.append(item.model_dump())
                else:
                    new_list.append(item)

            obj.set_editor_property(key, new_list)
            print(f"Set list {key} = {new_list}")
            continue
        #普通类型
        else:
            try: 
                obj.set_editor_property(key, value) 
                print(f"Set {key} = {value}") 
            except Exception as e: 
                print(f"[属性写入失败] {key}={value}, 错误: {e}")



def get_unreal_class(class_name: str): 
    """ 动态获取 Unreal 类型
    Example: 
        Input: “ChaosWheeledVehicleMovementComponent”
        Return: unreal.ChaosWheeledVehicleMovementComponent
    Or load Blueprint Class with path.
        Input:  "/Game/BP_TestActor"
        Return: unreal.load_class("/Game/BP_TestActor.BP_TestActor_C") #Type BlueprintGeneratedClass
    # clsa = get_unreal_class('ChaosWheeledVehicleMovementComponent')
    # clsb = get_unreal_class('/Game/Game/Generated/BP_TestActor')
    
    # # If callable
    # cls = unreal.ChaosWheeledVehicleMovementComponent
    # obj = cls()
    # print(obj)


    """
    # if type_path.startswith("unreal."): 
    #     try: 
    #         return eval(type_path) 
    #     except Exception: 
    #         pass
    if '/' in class_name or '\\' in class_name :
        return unreal.EditorAssetLibrary.load_blueprint_class(class_name)

    # 2. 尝试从 unreal 模块直接 getattr 
    if hasattr(unreal, class_name): 
        return getattr(unreal, class_name)
    
    raise Exception(f"No {class_name} in unreal.")

def get_cdo_components(class_path: str) -> dict:
    """
    传入蓝图“类路径”或“资产路径”都可以，比如：
    /Game/Game/Generated/BP_TestActor
    """
    # 关键：用 EditorAssetLibrary.load_blueprint_class，而不是 load_object
    bp_class = unreal.EditorAssetLibrary.load_blueprint_class(class_path)
    if bp_class is None:
        raise ValueError(f"无法加载 BlueprintGeneratedClass: {class_path}")

    # 关键：用全局的 get_default_object，比 bp_class.get_default_object 更稳
    # 就是这句改动起了效果
    cdo = unreal.get_default_object(bp_class)

    # 调试一下，先确认类型
    unreal.log(f"bp_class = {bp_class}, type = {type(bp_class)}")
    unreal.log(f"cdo      = {cdo}, type = {type(cdo)}")

    if not isinstance(cdo, unreal.Actor):
        raise TypeError(f"CDO 不是 Actor，而是 {type(cdo)}，蓝图父类可能不是 Actor 系列")

    comps = cdo.get_components_by_class(unreal.ActorComponent)
    return {c.get_name(): c for c in comps}



