# SkeletalMeshComponent
from dsl.models.registry import register_component,register_properties
from pydantic import BaseModel

@register_component("SkeletalMeshComponent", is_scene=True)
@register_properties("SkeletalMeshComponent")
class SkeletalMeshComponentProperties(BaseModel):
    pass

print("SkeletalMeshComponent Registered!")