from dsl.models.registry import register_component,register_properties
from pydantic import BaseModel
from typing import Dict, List, Optional,Any

# ------------------------------------------------------------
# 基础类型
# ------------------------------------------------------------

class EngineConfig(BaseModel):
    MaxRPM: Optional[int] = None
    # TorqueCurve: Optional[Dict[str, Any]] = None # Can't edit curve
    EngineIdleRPM: Optional[float] = None
    EngineBrakeEffect: Optional[float] = None
    # EngineInertia: Optional[float] = None # No such 


class TransmissionConfig(BaseModel):
    model_config = {
        "extra": "forbid"
    }

    bUseAutomaticGears: Optional[bool] = None
    FinalRatio: Optional[float] = None
    GearChangeTime: Optional[float] = None
    TransmissionEfficiency: Optional[float] = None
    ChangeUpRPM: Optional[float] = None 
    ChangeDownRPM: Optional[float] = None 
    ForwardGearRatios: Optional[List[float]] = None  # 每个档位的 GearRatio
    ReverseGearRatios: Optional[List[float]] = None  # 每个档位的 GearRatio


    #Example
    # bUseAutomaticGears: true
    # FinalRatio: 3.42
    # GearChangeTime: 0.25
    # TransmissionEfficiency: 0.98
    # ChangeUpRPM: 3000
    # ChangeDownRPM: 1500
    # ForwardGearRatios: [3.1, 2.2, 1.6, 1.2, 1.0, 0.85]
    # ReverseGearRatios: [2.86,2.86]


class DifferentialConfig(BaseModel):
    DifferentialType: Optional[str] = None  # LimitedSlip, Open, etc.
    FrontRearSplit: Optional[float] = None
    LeftRightSplit: Optional[float] = None
    CenterBias: Optional[float] = None
    FrontBias: Optional[float] = None
    RearBias: Optional[float] = None


class SuspensionConfig(BaseModel):
    SpringRate: Optional[float] = None
    SpringPreload: Optional[float] = None
    ShockStiffness: Optional[float] = None
    ShockDamping: Optional[float] = None
    MaxRaise: Optional[float] = None
    MaxDrop: Optional[float] = None


class WheelConfig(BaseModel):
    WheelClass: Optional[str] = None
    BoneName: Optional[str] = None
    AdditionalOffset: Optional[List[float]] = None  # X,Y,Z
    bAffectedByHandbrake: Optional[bool] = None
    bAffectedBySteering: Optional[bool] = None
    WheelRadius: Optional[float] = None
    WheelWidth: Optional[float] = None
    TireFrictionMultiplier: Optional[float] = None
    Suspension: Optional[SuspensionConfig] = None


class AerodynamicsConfig(BaseModel):
    DragCoefficient: Optional[float] = None
    DownforceCoefficient: Optional[float] = None


class SteeringConfig(BaseModel):
    SteeringCurve: Optional[Dict[str, float]] = None  # Speed → SteeringAngle
    MaxSteeringAngle: Optional[float] = None


class BrakeConfig(BaseModel):
    MaxBrakeTorque: Optional[float] = None
    MaxHandbrakeTorque: Optional[float] = None


# ------------------------------------------------------------
# ChaosWheeledVehicleMovementComponent 主配置
# ------------------------------------------------------------

@register_component("ChaosWheeledVehicleMovementComponent", is_scene=False)
@register_properties("ChaosWheeledVehicleMovementComponent")
class ChaosWheeledVehicleMovementProperties(BaseModel):
    model_config = {
        "extra": "forbid"
    }

    # 基础动力学
    Mass: Optional[float] = None
    DragCoefficient: Optional[float] = None
    CenterOfMassOverride: Optional[List[float]] = None  # X,Y,Z

    # 引擎
    EngineSetup: Optional[EngineConfig] = None

    # 传动
    TransmissionSetup: Optional[TransmissionConfig] = None

    # 差速器
    DifferentialSetup: Optional[DifferentialConfig] = None

    # 轮子数组
    Wheels: Optional[List[WheelConfig]] = None

    # 刹车
    BrakingSetup: Optional[BrakeConfig] = None

    # 空气动力学
    AeroSetup: Optional[AerodynamicsConfig] = None

    # 转向
    SteeringSetup: Optional[SteeringConfig] = None

    # 其他可选参数
    MaxSteeringAngle: Optional[float] = None
    MaxSpeed: Optional[float] = None
    bUseAckermannSteering: Optional[bool] = None


print("ChaosWheeledVehicleMovementComponent Registered!")