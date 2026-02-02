from typing import Dict, Any, List
from pydantic import BaseModel
from .scene_component_model import SceneComponentModel
from .non_scene_component_model import NonSceneComponentModel


class ChildActorModel(BaseModel):
    class_name: str
    properties: Dict[str, Any] = {}
    children: List[SceneComponentModel] = []
    components: List[NonSceneComponentModel] = []
