from typing import List, Optional
from pydantic import BaseModel, field_validator


class Transform(BaseModel):
    location: Optional[List[float]] = None
    rotation: Optional[List[float]] = None
    scale: Optional[List[float]] = None

    @field_validator("location", "rotation", "scale")
    @classmethod
    def check_vec3(cls, v):
        if v is None:
            return v
        if len(v) != 3:
            raise ValueError("Transform vector must have exactly 3 elements")
        return v
