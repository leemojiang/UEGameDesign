## 加载资产蓝图（Blueprint）

```python
bp = unreal.load_object(None,  r"/Game/Game/Generated/BP_TestActor2")
print(type(bp))
# <class 'Blueprint'>
```

## 加载蓝图类型（BlueprintGeneratedClass）
```python
bp_class = unreal.EditorAssetLibrary.load_blueprint_class(r"/Game/Game/Generated/BP_TestActor2")
print(f"bp_class = {bp_class}, type = {type(bp_class)}")
# bp_class = <Object '/Game/Game/Generated/BP_TestActor2.BP_TestActor2_C' (0x000002499D517700) Class 'BlueprintGeneratedClass'>, type = <class 'BlueprintGeneratedClass'>
```

## 获取Class Default Objects办法
```python
cdo = bp_class.get_default_object()
print(f"Loaded CDO: {cdo} {type(cdo)}")

#这种是有效的
cdo2 = unreal.get_default_object(bp_class)
print(f"Loaded CDO2: {cdo2} {type(cdo2)}")
# Loaded CDO: <Object '/Script/Engine.Default__BlueprintGeneratedClass' (0x0000024A82C65B00) Class 'BlueprintGeneratedClass'> <class 'BlueprintGeneratedClass'>
# Loaded CDO2: <Object '/Game/Game/Generated/BP_TestActor2.Default__BP_TestActor2_C' (0x0000024B40C15500) Class 'BP_TestActor2_C'> <class 'Actor'>
```

## 获取CDO的Components
```python
comps = cdo2.get_components_by_class(unreal.ActorComponent)
print([c.get_name() for c in comps])
```

## 管理蓝图的Components
但是Components的管理，不能用CDO，要用SubObject系统.

REF: 
    https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/SubobjectDataSubsystem?application_version=5.4#unreal.SubobjectDataSubsystem
    https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/SubobjectDataBlueprintFunctionLibrary?application_version=5.4#unreal-subobjectdatablueprintfunctionlibrary

    https://forums.unrealengine.com/t/editor-python-script-how-to-add-component-to-actor/1039923

    https://forums.unrealengine.com/t/python-trying-to-create-subobject-in-blueprint-getting-not-valid-handles/855866

    https://forums.unrealengine.com/t/opportunity-to-change-variables-in-blueprint-assets/2551047

    