from dsl.models.registry import register_component,register_properties
from pydantic import BaseModel
from typing import Dict

class EngineConfig(BaseModel):
    MaxRPM: int | None = None
    TorqueCurve: Dict[str, float] | None = None

@register_component("ChaosWheeledVehicleMovementComponent", is_scene=False)
@register_properties("ChaosWheeledVehicleMovementComponent")
class ChaosWheeledVehicleMovementProperties(BaseModel):
    model_config = { 
        "extra": "forbid" 
    }
    DragCoefficient: float| None = None
    EngineSetup: EngineConfig | None = None





print("ChaosWheeledVehicleMovementComponent Registered!")