from typing import Optional
from dsl.models.registry import register_component,register_properties
from pydantic import BaseModel

@register_component("CameraComponent",is_scene=True)
@register_properties("CameraComponent")
class CameraComponentProperties(BaseModel):
    model_config = {"extra": "allow"}

    # FieldOfView: 90.0
    # bUsePawnControlRotation: true

    FieldOfView: Optional[float] = None
    bUsePawnControlRotation: Optional[bool] = None

