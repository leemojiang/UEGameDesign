from dsl.models.registry import register_component, register_properties
from pydantic import BaseModel, field_serializer
from typing import Dict, List, Optional, Any
from dsl.models.properties.CurveFloat import CurveFloat
# ------------------------------------------------------------
# 基础类型
# ------------------------------------------------------------


class EngineConfig(BaseModel):
    model_config = {"extra": "forbid"}

    # Example
    # MaxTorque: 5000
    # MaxRPM: 7900
    # EngineIdleRPM: 900
    # EngineBrakeEffect: 0.15
    # EngineRevUpMOI : 5.0
    # EngineRevDownRate: 500
    # TorqueCurve:  #Can't edit Curve
    #   ExternalCurve: /Game/Game/Generated/MyCurve.MyCurve

    MaxTorque: Optional[float] = None
    MaxRPM: Optional[int] = None
    EngineIdleRPM: Optional[float] = None
    EngineBrakeEffect: Optional[float] = None
    EngineRevUpMOI: Optional[float] = None
    EngineRevDownRate: Optional[float] = None
    TorqueCurve: Optional[CurveFloat] = None


class TransmissionConfig(BaseModel):
    model_config = {"extra": "forbid"}

    bUseAutomaticGears: Optional[bool] = None
    FinalRatio: Optional[float] = None
    GearChangeTime: Optional[float] = None
    TransmissionEfficiency: Optional[float] = None
    ChangeUpRPM: Optional[float] = None
    ChangeDownRPM: Optional[float] = None
    ForwardGearRatios: Optional[List[float]] = None  # 每个档位的 GearRatio
    ReverseGearRatios: Optional[List[float]] = None  # 每个档位的 GearRatio

    # Example
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

    @field_serializer("DifferentialType")
    def serialize_diff(self, v, _info):
        import unreal

        if v == "ALL_WHEEL_DRIVE":
            # print("!!! AllWheelDrive")
            return unreal.VehicleDifferential.ALL_WHEEL_DRIVE
        elif v == "FRONT_WHEEL_DRIVE":
            return unreal.VehicleDifferential.FRONT_WHEEL_DRIVE
        elif v == "REAR_WHEEL_DRIVE":
            return unreal.VehicleDifferential.REAR_WHEEL_DRIVE
        return v


class SuspensionConfig(BaseModel):
    SpringRate: Optional[float] = None
    SpringPreload: Optional[float] = None
    ShockStiffness: Optional[float] = None
    ShockDamping: Optional[float] = None
    MaxRaise: Optional[float] = None
    MaxDrop: Optional[float] = None


class ChaosWheelSetup(BaseModel):
    WheelClass: Optional[str] = None
    BoneName: Optional[str] = None
    AdditionalOffset: Optional[List[float]] = None  # X,Y,Z

    def to_unreal(self, *args, **kwargs):
        import unreal
        from dsl.builder.ue_reflection import get_unreal_class

        data = self.model_dump(*args, **kwargs)

        wheel = unreal.ChaosWheelSetup()

        for key, value in data.items():
            if value is None:
                continue
            # 1. WheelClass: string → UClass
            if key == "WheelClass":
                cls = get_unreal_class(value)
                if cls:
                    wheel.set_editor_property("wheel_class", cls)
                else:
                    unreal.log_warning(f"WheelClass {value} not found.")
                continue

            # 2. AdditionalOffset: list → FVector
            if key == "AdditionalOffset":
                wheel.set_editor_property("additional_offset", unreal.Vector(*value))
                continue

            # 4. 默认处理：字段名转小写 → set_editor_property
            wheel.set_editor_property(key.lower(), value)

        return wheel


class SteeringConfig(BaseModel):
    SteeringCurve: Optional[CurveFloat] = None  # Speed → SteeringAngle
    AngleRatio: Optional[float] = None


# ------------------------------------------------------------
# ChaosWheeledVehicleMovementComponent 主配置
# ------------------------------------------------------------


@register_component("ChaosWheeledVehicleMovementComponent", is_scene=False)
@register_properties("ChaosWheeledVehicleMovementComponent")
class ChaosWheeledVehicleMovementProperties(BaseModel):
    model_config = {"extra": "allow"}

    # 基础动力学 VehicleSetups
    Mass: Optional[float] = None
    DragCoefficient: Optional[float] = None
    CenterOfMassOverride: Optional[List[float]] = None  # X,Y,Z
    DownforceCoefficient: Optional[float] = None

    # 引擎
    EngineSetup: Optional[EngineConfig] = None

    # 传动
    TransmissionSetup: Optional[TransmissionConfig] = None

    # 差速器
    DifferentialSetup: Optional[DifferentialConfig] = None

    # 轮子数组
    WheelSetups: Optional[List[ChaosWheelSetup]] = None

    # 转向
    SteeringSetup: Optional[SteeringConfig] = None

    @field_serializer("WheelSetups")
    def serialize_wheelSetups(self, wheels, _info):
        return [wheel.to_unreal() for wheel in wheels]


print("ChaosWheeledVehicleMovementComponent Registered!")
