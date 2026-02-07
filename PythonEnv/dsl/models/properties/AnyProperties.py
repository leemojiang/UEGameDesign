from pydantic import BaseModel
from dsl.models.registry import register_properties


# AnyProperties 用于处理未知的 Actor / Component Properties
@register_properties("AnyProperties")
class AnyProperties(BaseModel):
    model_config = {"extra": "allow"}
