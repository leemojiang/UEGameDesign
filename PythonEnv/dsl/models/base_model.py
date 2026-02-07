from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class Transform(BaseModel):
    relative_location: Optional[List[float]] = Field(alias="location",default=None)
    relative_rotation: Optional[List[float]] = Field(alias="rotation",default=None)
    relative_scale: Optional[List[float]] = Field(alias="scale",default=None)
    bAbsoluteLocation: Optional[bool] = None
    bAbsoluteRotation: Optional[bool] = None    
    bAbsoluteScale: Optional[bool] = None

    @field_validator("relative_location", "relative_rotation", "relative_scale")
    @classmethod
    def check_vec3(cls, v):
        if v is None:
            return v
        if len(v) != 3:
            raise ValueError("Transform vector must have exactly 3 elements")
        return v
