from pydantic import BaseModel
import unreal
from dsl.models.registry import register_properties
import os

# AnyProperties 用于处理未知的 Actor / Component Properties
@register_properties("AnyProperties")
class AnyProperties(BaseModel):
    model_config = {"extra": "allow"}

    def model_dump(self, *args, **kwargs):
        raw = super().model_dump(*args, **kwargs)
        return { key: self.__getitem__(key) for key in raw }


    def __getitem__(self, key):
        value = getattr(self, key, None)
        if isinstance(value, str) and self._is_asset_path(value):
            print(f"Loading asset for property '{key}': {value}")
            return self._load_asset(value)
        return value

    def _is_asset_path(self, value: str) -> bool:
        # 简单判断是否为uasset路径
        return  value.startswith("/Game/") or value.startswith("/Engine/")

    def _load_asset(self, path: str):
        # 这里简单返回路径，实际可替换为资源加载逻辑
        # 比如调用UE的API加载资源
        asset = unreal.load_asset(path)
        if not asset:
            unreal.log_warning(f"无法加载资源: {path}")
        return asset
