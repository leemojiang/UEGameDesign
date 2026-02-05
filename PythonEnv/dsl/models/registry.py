# 简单版本：手工维护，后面可以改成从 UE 反射生成

SCENE_COMPONENTS = {
    "SceneComponent",
    "StaticMeshComponent",
    "CameraComponent",
    "SpringArmComponent",
    "CapsuleComponent",
    "SkeletalMeshComponent",
}

NON_SCENE_COMPONENTS = {
    # "ChaosWheeledVehicleMovementComponent",
    "CharacterMovementComponent",
    "ProjectileMovementComponent",
}


from typing import Dict, Type
from pydantic import BaseModel

# ============================================================
# 1. 全局 Properties Schema 注册表
# ============================================================

PROPERTY_SCHEMA_REGISTRY: Dict[str, Type[BaseModel]] = {}


def register_properties(component_type: str):
    """
    装饰器:注册某个组件类型的 properties schema。
    """
    def decorator(cls: Type[BaseModel]):
        PROPERTY_SCHEMA_REGISTRY[component_type] = cls
        return cls
    return decorator

def register_component(component_type: str , is_scene: bool = True):
    """
    装饰器:注册某个组件是否是scene类型.
    """
    def decorator(cls: Type[BaseModel]):
        if is_scene:
            SCENE_COMPONENTS.add(component_type)
        else:
            NON_SCENE_COMPONENTS.add(component_type)
        return cls
    return decorator

# Execute Auto registry
# Make sure all decorator is defined
# Avoid Loop import
import dsl.models.properties
