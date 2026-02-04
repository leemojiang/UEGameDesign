import unreal

def apply_properties(obj, props: dict):
    for key, value in props.items():
        if isinstance(value, dict):
            sub = obj.get_editor_property(key)
            apply_properties(sub, value)
            obj.set_editor_property(key, sub)
        else:
            
            try:
                obj.set_editor_property(key, value)
                print(f"Set {key} : {value} for {obj}")
            except Exception as e:
                unreal.log_warning(f"[Actor属性失败] {key}={value}, 错误: {e}")

new_asset_path = r"/Game/Game/Generated/BP_TestActor"
# 加载蓝图类``
cls = unreal.EditorAssetLibrary.load_blueprint_class(new_asset_path)
cdo = unreal.get_default_object(cls)

# 获取 MovementComponent
movement = cdo.get_component_by_class(unreal.ChaosWheeledVehicleMovementComponent)

#Properties 
prop = {"EngineSetup" : {"MaxRPM": 8000} }


apply_properties(movement,prop)

# # 1. 取出 EngineSetup 结构体 
# engine = movement.get_editor_property("EngineSetup")
# print(type(engine))
# print(dir(engine))
# print(engine.export_text())
# engine.set_editor_property("MaxRPM", 8000)
# movement.set_editor_property("EngineSetup", engine)

# movement.set_editor_property(**engine)

# transmission = movement.get_editor_property("TransmissionSetup")
# print(type(transmission))
# print(dir(transmission))
# print(transmission.export_text())
# movement.set_editor_property("TransmissionSetup", transmission)

# wheels = movement.get_editor_property("WheelSetups")

# new_wheel = unreal.ChaosWheelSetup()
# print(type(new_wheel))
# print(dir(new_wheel))
# print(new_wheel.export_text())
# new_wheel.set_editor_property("BoneName", "Wheel_FL") 
# new_wheel.set_editor_property("AdditionalOffset", unreal.Vector(0, 0, 0)) 
# # new_wheel.set_editor_property("bDisableSteering", False) 
# # new_wheel.set_editor_property("bAffectedByHandbrake", False)
# wheels.append(new_wheel)
# movement.set_editor_property("WheelSetups", wheels)



# unreal.Object.set_editor_property(engine, "MaxRPM", 7000)