from typing import Optional
from pydantic import BaseModel, field_serializer
from dsl.builder.ue_reflection import get_unreal_class, create_unreal_asset
import unreal

# Base Date asset/types.
class CurveFloat(BaseModel):
    ExternalCurve: Optional[str] = None # '/Game/Game/Generated/MyCurve.MyCurve'
    #<Object '/Game/Game/Generated/MyCurve.MyCurve' (0x000001D2FA1D2100) Class 'CurveFloat'>

    @field_serializer("ExternalCurve")
    def serialize_external_curve(self, curve_path, _info):
        if curve_path:
            curve_obj = unreal.load_asset(curve_path)
            if curve_obj:
                return curve_obj
            else:
                unreal.log_warning(f"无法加载曲线资源: {curve_path}，将尝试创建新资源。")
                return create_unreal_asset(curve_path, "CurveFloat")
        return None
