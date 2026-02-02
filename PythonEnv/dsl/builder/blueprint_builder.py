import unreal
from dsl.builder.component_builder import ComponentBuilder
from dsl.models.actor_model import ActorModel


class BlueprintBuilder:

    def asset_exists(self,asset_path: str) -> bool: 
        return unreal.EditorAssetLibrary.does_asset_exist(asset_path)

    def create_blueprint_from_model(self, model: ActorModel, new_asset_path: str):
        if self.asset_exists(new_asset_path):
            raise FileExistsError(f"资产已存在: {new_asset_path}")

        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        factory = unreal.BlueprintFactory()

        # 自动补 _C
        parent_path = model.class_name
        if not parent_path.endswith("_C"):
            parent_path += "_C"

        parent_class = unreal.load_object(None, parent_path)
        if parent_class is None:
            raise ValueError(f"无法加载父类蓝图: {parent_path}")

        factory.set_editor_property("ParentClass", parent_class)

        blueprint = asset_tools.create_asset(
            asset_name=new_asset_path.split("/")[-1],
            package_path="/".join(new_asset_path.split("/")[:-1]),
            asset_class=unreal.Blueprint,
            factory=factory
        )

        if blueprint is None:
            raise RuntimeError(f"蓝图创建失败: {new_asset_path}")

        unreal.EditorAssetLibrary.save_asset(new_asset_path)
        unreal.EditorAssetLibrary.sync_browser_to_objects([blueprint])

        return blueprint


    def tweak_blueprint_from_model(self, model: ActorModel, new_asset_path: str):

        # 加载 BlueprintGeneratedClass
        bp_class = unreal.EditorAssetLibrary.load_blueprint_class(new_asset_path)
        if bp_class is None:
            raise RuntimeError(f"无法加载 BlueprintGeneratedClass: {new_asset_path}")

        cdo = unreal.get_default_object(bp_class)        
        print(f"Loaded CDO: {cdo} Type={type(cdo)}")
        
        if cdo is None:
            raise RuntimeError(f"无法加载蓝图的 CDO: {new_asset_path}")

        # 使用当前蓝图路径，而不是父类路径
        builder = ComponentBuilder(cdo, new_asset_path)

        # NonSceneComponent
        for comp in model.components:
            builder.build_non_scene_component(comp)

        # SceneComponent
        for sc in model.children:
            builder.build_scene_component(sc, None)

        # Actor 属性
        self._apply_actor_properties(cdo, model.properties)

        # transform 不适用于 CDO，跳过

        # 保存蓝图
        unreal.EditorAssetLibrary.save_asset(new_asset_path)

        # # 同步到资产（不是类）
        # blueprint = unreal.load_object(None, new_asset_path)
        # unreal.EditorAssetLibrary.sync_browser_to_objects([blueprint])

    # ------------------------
    # 辅助函数
    # ------------------------

    def _apply_actor_properties(self, actor, props: dict):
        for key, value in props.items():
            try:
                actor.set_editor_property(key, value)
            except Exception as e:
                unreal.log_warning(f"[Actor属性失败] {key}={value}, 错误: {e}")

    def _apply_actor_transform(self, actor, transform):
        if transform.location:
            actor.set_actor_relative_location(unreal.Vector(*transform.location))
        if transform.rotation:
            actor.set_actor_relative_rotation(unreal.Rotator(*transform.rotation))
        if transform.scale:
            actor.set_actor_relative_scale3d(unreal.Vector(*transform.scale))
