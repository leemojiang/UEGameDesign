from dsl.models.registry import register_component,register_properties
from pydantic import BaseModel, field_serializer
from typing import List, Optional, Dict

@register_component("SpringArmComponent",is_scene=True)
@register_properties("SpringArmComponent")
class SpringArmComponentProperties(BaseModel):
    model_config = {"extra": "allow"}
    
    # Example properties for SpringArmComponent
    # TargetArmLength: 300.0
    # TargetOffset: [0.0, 0.0, 50.0]
    # SocketOffset: [0.0, 0.0, 0.0]

    # bEnableCameraLag: true
    # CameraLagSpeed: 3.0
    # bUsePawnControlRotation: true

    # ProbeSize: 12.0
    # bDoCollisionTest: true

    TargetArmLength: Optional[float] = None
    TargetOffset: Optional[List[float]] = None  # X,Y,Z offset
    SocketOffset: Optional[List[float]] = None  # X,Y,Z offset

    bEnableCameraLag: Optional[bool] = None
    CameraLagSpeed: Optional[float] = None
    bUsePawnControlRotation: Optional[bool] = None

    ProbeSize: Optional[float] = None
    bDoCollisionTest: Optional[bool] = None
    