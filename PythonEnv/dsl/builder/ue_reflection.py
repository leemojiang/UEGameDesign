# dsl/builder/ue_reflection.py
import unreal

# def get_default_components(class_path: str) -> dict:
#     """
#     返回蓝图类默认组件的字典 {component_name: component_object}
#     """

#     # 使用 load_blueprint_class，而不是 load_object
#     # cls = unreal.load_object(None, class_path)
#     cls = unreal.EditorAssetLibrary.load_blueprint_class(class_path)
#     if cls is None:
#         raise ValueError(f"无法加载 BlueprintGeneratedClass: {class_path}")

#     cdo = cls.get_default_object() #就改了这句
#     print(f"cdo      = {cdo}, type = {type(cdo)}")

#     comps = cdo.get_components_by_class(unreal.ActorComponent)

#     return {c.get_name(): c for c in comps}

import unreal

def get_default_components(class_path: str) -> dict:
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



