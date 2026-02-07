# SkeletalMeshComponent
from dsl.models.registry import register_component,register_properties
from pydantic import BaseModel, field_serializer
from typing import List, Optional, Dict
import unreal

# ------------------------------------------------------------
# 子类型：LOD 配置
# ------------------------------------------------------------

class SkeletalMeshLODMaterialConfig(BaseModel):
    MaterialSlotName: Optional[str] = None
    MaterialPath: Optional[str] = None


class SkeletalMeshLODConfig(BaseModel):
    ScreenSize: Optional[float] = None
    ReductionSettings: Optional[Dict[str, float]] = None  # PercentTriangles, MaxDeviation, etc.
    Materials: Optional[List[SkeletalMeshLODMaterialConfig]] = None


# ------------------------------------------------------------
# 子类型：Physics 配置
# ------------------------------------------------------------

class SkeletalMeshPhysicsConfig(BaseModel):
    bEnablePerPolyCollision: Optional[bool] = None
    PhysicsAsset: Optional[str] = None
    ShadowPhysicsAsset: Optional[str] = None
    bUseAsyncScene: Optional[bool] = None


# ------------------------------------------------------------
# 子类型：Socket 配置
# ------------------------------------------------------------

class SkeletalMeshSocketConfig(BaseModel):
    SocketName: Optional[str] = None
    BoneName: Optional[str] = None
    RelativeLocation: Optional[List[float]] = None  # X,Y,Z
    RelativeRotation: Optional[List[float]] = None  # Pitch,Yaw,Roll
    RelativeScale: Optional[List[float]] = None     # X,Y,Z


# ------------------------------------------------------------
# 子类型：Bounds 配置
# ------------------------------------------------------------

class SkeletalMeshBoundsConfig(BaseModel):
    Origin: Optional[List[float]] = None
    BoxExtent: Optional[List[float]] = None
    SphereRadius: Optional[float] = None


# ------------------------------------------------------------
# 子类型：Animation 配置
# ------------------------------------------------------------

class SkeletalMeshAnimationConfig(BaseModel):
    AnimClass: Optional[str] = None
    DefaultSlotNode: Optional[str] = None
    bEnableRootMotion: Optional[bool] = None
    RootMotionMode: Optional[str] = None  # e.g. "RootMotionFromMontagesOnly"


# ------------------------------------------------------------
# 子类型：Import 信息
# ------------------------------------------------------------

class SkeletalMeshImportConfig(BaseModel):
    SourceFile: Optional[str] = None
    ImportScale: Optional[List[float]] = None
    bImportMorphTargets: Optional[bool] = None
    bPreserveSmoothingGroups: Optional[bool] = None


# ------------------------------------------------------------
# 主类型：SkeletalMesh 配置
# ------------------------------------------------------------

@register_component("SkeletalMeshComponent", is_scene=False)
@register_properties("SkeletalMeshComponent")
class SkeletalMeshComponentProperties(BaseModel):
    model_config = {
        "extra": "allow"
    }

    # 基础属性
    SkeletalMeshAsset: Optional[str] = None
    # SkeletonPath: Optional[str] = None
    # Materials: Optional[List[str]] = None

    # # LODs
    # LODSettings: Optional[List[SkeletalMeshLODConfig]] = None

    # # Physics
    # PhysicsSetup: Optional[SkeletalMeshPhysicsConfig] = None

    # # Sockets
    # Sockets: Optional[List[SkeletalMeshSocketConfig]] = None

    # # Bounds
    # Bounds: Optional[SkeletalMeshBoundsConfig] = None

    # # Animation
    # AnimationSetup: Optional[SkeletalMeshAnimationConfig] = None

    # # Import 信息
    # ImportSettings: Optional[SkeletalMeshImportConfig] = None

    # # 其他可选属性
    # bEnableShadowCasting: Optional[bool] = None
    # bUseHighPrecisionTangents: Optional[bool] = None
    # bSupportRayTracing: Optional[bool] = None

    @field_serializer("SkeletalMeshAsset")
    def serialize_wheelSetups(self, mesh_path, _info):
        return unreal.load_asset(mesh_path) if mesh_path else None


print("SkeletalMeshComponent Registered!")