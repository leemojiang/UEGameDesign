import unreal

bp_class = unreal.EditorAssetLibrary.load_blueprint_class(r"/Game/Game/Generated/BP_TestActor2")
# print(f"bp_class = {bp_class}, type = {type(bp_class)}")
# bp_class = <Object '/Game/Game/Generated/BP_TestActor2.BP_TestActor2_C' (0x000002499D517700) Class 'BlueprintGeneratedClass'>, type = <class 'BlueprintGeneratedClass'>

cdo = bp_class.get_default_object()
# print(f"Loaded CDO: {cdo} {type(cdo)}")

#这种是有效的
cdo2 = unreal.get_default_object(bp_class)
# print(f"Loaded CDO2: {cdo2} {type(cdo2)}")
# Loaded CDO: <Object '/Script/Engine.Default__BlueprintGeneratedClass' (0x0000024A82C65B00) Class 'BlueprintGeneratedClass'> <class 'BlueprintGeneratedClass'>
# Loaded CDO2: <Object '/Game/Game/Generated/BP_TestActor2.Default__BP_TestActor2_C' (0x0000024B40C15500) Class 'BP_TestActor2_C'> <class 'Actor'>



