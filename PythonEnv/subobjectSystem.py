import unreal

sds = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem) 
new_asset_path = r"/Game/Game/Generated/BP_TestActor"
# 加载蓝图类``
actor = unreal.EditorAssetLibrary.load_blueprint_class(new_asset_path)
bp = unreal.load_object(None, new_asset_path)

subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
BFL = unreal.SubobjectDataBlueprintFunctionLibrary
print([BFL.is_handle_valid(x) for x in subsystem.k2_gather_subobject_data_for_blueprint(context=bp)])
# print([BFL.is_handle_valid(x) for x in subsystem.k2_gather_subobject_data_for_instance(context=actor)])

# print(dir([BFL.is_handle_valid(x) for x in subsystem.k2_gather_subobject_data_for_blueprint(context=bp)][0]))

handles = subsystem.k2_gather_subobject_data_for_blueprint(context=bp)

print(dir(BFL))

for handle in handles:
    data = BFL.get_data(handle)

    obj = BFL.get_object(data)
    BFL.get_name(data)
    print(obj)
    # obj.set_editor_property("BoneName", "Wheel_FL")
   

print(type(obj))
obj.set_editor_property("DragCoefficient", 0.80)