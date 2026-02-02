from typing import Any, Dict, List

from dsl.models.actor_model import ActorModel
from dsl.models.scene_component_model import SceneComponentModel
from dsl.models.non_scene_component_model import NonSceneComponentModel
from dsl.models.child_actor_model import ChildActorModel
from dsl.models.registry import SCENE_COMPONENTS, NON_SCENE_COMPONENTS


class ObjectParser:
    """负责把 YAML dict 解析成 ActorModel / SceneComponentModel 等"""

    def parse(self, data: Dict[str, Any]) -> ActorModel:
        if "Object" not in data:
            raise ValueError("顶层必须包含 Object 字段")

        obj = data["Object"]

        children = self._parse_scene_components(obj.get("children", []))
        components = self._parse_non_scene_components(obj.get("components", []))

        actor = ActorModel(
            class_name=obj["class"],
            name=obj.get("name", obj["class"]),
            transform=obj.get("transform"),
            properties=obj.get("properties", {}),
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
                properties=item.get("properties", {}),
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

            model = NonSceneComponentModel(
                type=comp_type,
                name=item["name"],
                properties=item.get("properties", {}),
            )
            result.append(model)
        return result

    def _parse_child_actor(self, data: Dict[str, Any]) -> ChildActorModel:
        children = self._parse_scene_components(data.get("children", []))
        components = self._parse_non_scene_components(data.get("components", []))

        return ChildActorModel(
            class_name=data["class"],
            properties=data.get("properties", {}),
            children=children,
            components=components,
        )
