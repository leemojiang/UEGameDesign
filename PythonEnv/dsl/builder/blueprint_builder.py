from pydantic import BaseModel
import unreal
from dsl.builder.component_builder import ComponentBuilder
from dsl.models.actor_model import ActorModel
from dsl.builder.ue_reflection import get_unreal_class , apply_properties


class BlueprintBuilder:
    def __init__(self):
        self.comp_builder = ComponentBuilder()

    def asset_exists(self, asset_path: str) -> bool:
        return unreal.EditorAssetLibrary.does_asset_exist(asset_path)

    def create_blueprint_from_model(self, model: ActorModel, new_asset_path: str ,overwrite=False):
        if self.asset_exists(new_asset_path):
            if not overwrite:
                # raise FileExistsError(f"资产已存在: {new_asset_path}")
                print(f"资产已存在: {new_asset_path}")
                return unreal.load_object(None,new_asset_path)

        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        factory = unreal.BlueprintFactory()

        # 自动补 _C
        parent_path = model.class_name
        # if not parent_path.endswith("_C"):
        #     parent_path += "_C"

        parent_class = get_unreal_class(parent_path)
        if parent_class is None:
            raise ValueError(f"无法加载父类蓝图: {parent_path}")

        factory.set_editor_property("ParentClass", parent_class)

        blueprint = asset_tools.create_asset(
            asset_name=new_asset_path.split("/")[-1],
            package_path="/".join(new_asset_path.split("/")[:-1]),
            asset_class=unreal.Blueprint,
            factory=factory,
        )

        if blueprint is None:
            raise RuntimeError(f"蓝图创建失败: {new_asset_path}")

        unreal.EditorAssetLibrary.save_asset(new_asset_path)
        unreal.EditorAssetLibrary.sync_browser_to_objects([new_asset_path])

        return blueprint

    def tweak_blueprint_from_model(self, model: ActorModel, new_asset_path: str):
        # 加载 BlueprintGeneratedClass
        bp = unreal.load_object(None,new_asset_path)
        # ComponentBuilder needs BPasset rather BPgeneratedClass
        bp_asset = unreal.BlueprintEditorLibrary.get_blueprint_asset(bp)
        if bp_asset is None:
            raise RuntimeError(f"无法加载 BlueprintAsset: {new_asset_path}")
        
       
        # NonSceneComponent
        root_handle = self.comp_builder.get_actor_root_handle(bp_asset)
        # self.comp_builder.print_components_info(handles)
        for comp in model.components:
            comp_name = comp.name
            comp_class= get_unreal_class(comp.type)

            comp_handle, comp_obj = self.comp_builder.get_component(bp_asset,comp_name)
            
            if comp_obj:
                print(f"Comp {comp_name} {comp_class} Exists.") 
            else:
                comp_handle, comp_obj =self.comp_builder.add_component(root_handle,bp_asset,comp_class,comp_name)
                print(f"Comp {comp_name} {comp_class} Added.")

            properties_model = comp.properties
            apply_properties(comp_obj,properties_model.model_dump(serialize_as_any=True,exclude_none=True)) #comp properties dict
            # apply_basemodel_properties(comp_obj,properties_model)

        # SceneComponent
        for sc in model.children:
            self._build_scene_component(sc, bp_asset, root_handle)
        
        # Actor 属性
        # TODO
        
        # 保存蓝图
        unreal.EditorAssetLibrary.save_asset(new_asset_path)
        unreal.EditorAssetLibrary.sync_browser_to_objects([new_asset_path])

    # ------------------------
    # 辅助函数
    # ------------------------
    def _build_scene_component(self, comp_model,bp_asset, parent_handle):
        comp_name = comp_model.name
        comp_class= get_unreal_class(comp_model.type)

        comp_handle, comp_obj = self.comp_builder.get_component(bp_asset,comp_name)
        
        if comp_obj:
            print(f"Scene Comp {comp_name} {comp_class} Exists.") 
        else:
            comp_handle, comp_obj =self.comp_builder.add_component(parent_handle,bp_asset,comp_class,comp_name)
            print(f"Scene Comp {comp_name} {comp_class} Added.")

        properties_model = comp_model.properties
        apply_properties(comp_obj,properties_model.model_dump(serialize_as_any=True,exclude_none=True)) #comp properties dict

        if comp_model.transform:
            apply_properties(comp_obj,comp_model.transform.model_dump(exclude_none=True)) #comp properties dict

        # 递归子组件
        for child in comp_model.children:
            self._build_scene_component(child,bp_asset, comp_handle)


