from __future__ import annotations
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from .base_model import Transform


class SceneComponentModel(BaseModel):
    type: str
    name: str
    attach_to: Optional[str] = None
    transform: Optional[Transform] = None
    properties: BaseModel | Dict[str,Any] | None = None
    children: List["SceneComponentModel"] = []
    child_actor: Optional["ChildActorModel"] = None  # 由后面再绑定类型

from .child_actor_model import ChildActorModel
SceneComponentModel.model_rebuild()