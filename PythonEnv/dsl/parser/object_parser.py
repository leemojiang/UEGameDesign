from typing import Any, Dict, List

from dsl.models.actor_model import ActorModel
from dsl.models.scene_component_model import SceneComponentModel
from dsl.models.non_scene_component_model import NonSceneComponentModel
from dsl.models.child_actor_model import ChildActorModel
from dsl.models.registry import SCENE_COMPONENTS, NON_SCENE_COMPONENTS,PROPERTY_SCHEMA_REGISTRY


class ObjectParser:
    """负责把 YAML dict 解析成 ActorModel / SceneComponentModel 等"""

    def parse(self, data: Dict[str, Any]) -> ActorModel:
        if "Object" not in data:
            raise ValueError("顶层必须包含 Object 字段")

        obj = data["Object"]

        children = self._parse_scene_components(obj.get("children", []))
        components = self._parse_non_scene_components(obj.get("components", []))
        
        # Actor Properties 检查
        actor_class = obj.get("class")
        actor_schema = PROPERTY_SCHEMA_REGISTRY.get(actor_class)
        props = obj.get("properties", {}) or {}
        if not actor_schema: 
            # raise ValueError(f"Unknown Actor class: {actor_class}") 
            print(f"Unknown Actor class: {actor_class} Use AnyProperties instead.") 
            props = PROPERTY_SCHEMA_REGISTRY["AnyProperties"](**props)
        else:
            props = actor_schema(**props)

        actor = ActorModel(
            class_name=obj["class"],
            name=obj.get("name", obj["class"]),
            transform=obj.get("transform"),
            properties=props,
            children=children,
            components=components,
        )
        return actor

    def _parse_scene_components(self, items: List[Dict[str, Any]]) -> List[SceneComponentModel]:
        result: List[SceneComponentModel] = []
        for item in items:
            comp_type = item.get("type")
            if comp_type not in SCENE_COMPONENTS:
                raise ValueError(f"{comp_type} 不是 SceneComponent（或未在 registry 中注册）")

            # 找到 properties schema 
            schema = PROPERTY_SCHEMA_REGISTRY.get(comp_type) 
            if not schema: 
                # raise ValueError(f"Unknown component type: {comp_type}")
                print(f"Unknown component type: {comp_type} Use AnyProperties instead.")
                schema = PROPERTY_SCHEMA_REGISTRY["AnyProperties"] 
            
            raw_properties = item.get("properties", {}) or {}
            props = schema(**raw_properties)
            
            # 递归解析 children
            children = self._parse_scene_components(item.get("children", []))

            # 解析 child_actor（如果有）
            child_actor_data = item.get("child_actor")
            child_actor = None
            if child_actor_data:
                child_actor = self._parse_child_actor(child_actor_data)

            model = SceneComponentModel(
                type=comp_type,
                name=item["name"],
                attach_to=item.get("attach_to"),
                transform=item.get("transform"),
                properties=props,
                children=children,
                child_actor=child_actor,
            )
            result.append(model)
        return result

    def _parse_non_scene_components(self, items: List[Dict[str, Any]]) -> List[NonSceneComponentModel]:
        result: List[NonSceneComponentModel] = []
        for item in items:
            comp_type = item.get("type")
            if comp_type not in NON_SCENE_COMPONENTS:
                raise ValueError(f"{comp_type} 不是 NonSceneComponent（或未在 registry 中注册）")

            schema = PROPERTY_SCHEMA_REGISTRY.get(comp_type)
            if not schema:
                # raise ValueError(f"Unknown component type: {comp_type}")
                print(f"Unknown component type: {comp_type} Use AnyProperties instead.")
                schema = PROPERTY_SCHEMA_REGISTRY["AnyProperties"]
            
            raw_properties = item.get("properties", {}) or {}
            props = schema(**raw_properties)

            model = NonSceneComponentModel(
                type=comp_type,
                name=item["name"],
                properties=props,
            )

            result.append(model)
        return result

    def _parse_child_actor(self, data: Dict[str, Any]) -> ChildActorModel:
        children = self._parse_scene_components(data.get("children", []))
        components = self._parse_non_scene_components(data.get("components", []))

        return ChildActorModel(
            class_name=data["class"],
            properties=PROPERTY_SCHEMA_REGISTRY.get(data["class"], PROPERTY_SCHEMA_REGISTRY["AnyProperties"])(**data.get("properties", {})),
            children=children,
            components=components,
        )
