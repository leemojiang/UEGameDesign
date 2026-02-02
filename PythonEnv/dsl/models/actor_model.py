from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from .base_model import Transform
from .scene_component_model import SceneComponentModel
from .non_scene_component_model import NonSceneComponentModel


class ActorModel(BaseModel):
    class_name: str
    name: str
    transform: Optional[Transform] = None
    properties: Dict[str, Any] = {}
    children: List[SceneComponentModel] = []
    components: List[NonSceneComponentModel] = []
