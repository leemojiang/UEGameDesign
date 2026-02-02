# dsl/builder/component_builder.py
import unreal
from dsl.builder.ue_reflection import get_default_components
from dsl.models.non_scene_component_model import NonSceneComponentModel

class ComponentBuilder:

    def __init__(self, actor, blueprint_class_path: str):
        self.actor = actor
        self.default_components = get_default_components(blueprint_class_path)

    def build_non_scene_component(self, model:NonSceneComponentModel):
        """
        NonSceneComponentModel → UE Component
        避免重复添加蓝图默认组件
        """
        # 如果蓝图类已经有这个组件
        if model.name in self.default_components:
            comp = self.default_components[model.name]
            self._apply_properties(comp, model.properties)
            return comp

        # 否则创建新组件
        comp_class = unreal.find_class(model.type)
        comp = unreal.create_component(self.actor, comp_class, model.name)

        self._apply_properties(comp, model.properties)
        return comp

    def build_scene_component(self, model, parent=None):
        """
        SceneComponentModel → UE SceneComponent
        """
        comp_class = unreal.find_class(model.type)
        comp = unreal.create_component(self.actor, comp_class, model.name)

        # attach
        if parent:
            comp.attach_to_component(parent, "None", unreal.AttachmentRule.KEEP_RELATIVE)

        # transform
        if model.transform:
            self._apply_transform(comp, model.transform)

        # properties
        self._apply_properties(comp, model.properties)

        # children
        for child in model.children:
            self.build_scene_component(child, comp)

        # child_actor
        if model.child_actor:
            self._build_child_actor(comp, model.child_actor)

        return comp

    def _apply_transform(self, comp, transform):
        if transform.location:
            comp.set_relative_location(unreal.Vector(*transform.location))
        if transform.rotation:
            comp.set_relative_rotation(unreal.Rotator(*transform.rotation))
        if transform.scale:
            comp.set_relative_scale3d(unreal.Vector(*transform.scale))

    def _apply_properties(self, comp, props: dict):
        for key, value in props.items():
            try:
                unreal.Object.set_editor_property(comp, key, value)
            except Exception as e:
                unreal.log_warning(f"属性设置失败: {key}={value}, 错误: {e}")

    def _build_child_actor(self, parent_comp, child_model):
        """
        ChildActorModel → ChildActorComponent
        """
        child_comp = unreal.create_component(
            self.actor,
            unreal.ChildActorComponent,
            f"{child_model.class_name}_ChildActor"
        )

        child_comp.attach_to_component(parent_comp, "None", unreal.AttachmentRule.KEEP_RELATIVE)
        child_comp.set_child_actor_class(unreal.load_object(None, child_model.class_name))

        # 递归构建子 Actor 的组件
        child_actor = child_comp.get_child_actor()
        sub_builder = ComponentBuilder(child_actor, child_model.class_name)

        for c in child_model.components:
            sub_builder.build_non_scene_component(c)

        for sc in child_model.children:
            sub_builder.build_scene_component(sc, None)
