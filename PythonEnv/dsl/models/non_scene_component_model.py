from typing import Dict, Any
from pydantic import BaseModel


class NonSceneComponentModel(BaseModel):
    type: str
    name: str
    properties: BaseModel | Dict[str,Any] |None = None
