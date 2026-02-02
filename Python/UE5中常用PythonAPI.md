## 加载资产蓝图（Blueprint）

```python
bp = unreal.load_object(None,  r"/Game/Game/Generated/BP_TestActor2")
print(type(bp))
# <class 'Blueprint'>

# Converter to Makesure
bp_asset = unreal.BlueprintEditorLibrary.get_blueprint_asset(bp)
print(type(bp_asset))
# <class 'Blueprint'>
```
## 新建蓝图资产（Blueprint）
```python
factory = unreal.BlueprintFactory()
factory.set_editor_property("parent_class", unreal.Actor)

asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
blueprint = asset_tools.create_asset(asset_name, asset_dir, None, factory)
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
    https://www.unrealcode.net/PythonScripting

    https://forums.unrealengine.com/t/python-trying-to-create-subobject-in-blueprint-getting-not-valid-handles/855866

###
    https://forums.unrealengine.com/t/opportunity-to-change-variables-in-blueprint-assets/2551047
        Hi Levan,
        The recommended way to access blueprint components and script operations on them is to use the API provided by the SubobjectDataSubsystem and the SubobjectDataBlueprintFunctionLibrary. From your usage of “get_default_object(generated_class)”, I assume you are working with Python:

        subobject_subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)When using the SubobjectDataSubsystem, you can work directly with blueprint assets or actor instances, no need to access their generated class or default objects. Simply iterate over the components using one of these functions:

        subhandles = subobject_subsystem.k2_gather_subobject_data_for_instance(actor) subhandles = subobject_subsystem.k2_gather_subobject_data_for_blueprint(blueprint)The returned array will have a handle for the generated class as its first item, and the components following next, including native and blueprint, locally-defined or inherited. For example, here is a function to print some information about selected blueprint assets and all of their subobjects:

        `def print_selected_blueprint_subobjects_info():

        subobject_subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)

        selected_assets = unreal.EditorUtilityLibrary.get_selected_assets()for asset in selected_assets:blueprint = unreal.BlueprintEditorLibrary.get_blueprint_asset(asset)if unreal.SystemLibrary.is_valid(blueprint):unreal.log(“Class: “” + blueprint.get_name() + “” Name: “” + asset.get_name() + “” Path: “” + asset.get_path_name() + “””)subhandles = subobject_subsystem.k2_gather_subobject_data_for_blueprint(blueprint)for subhandle in subhandles:subdata = unreal.SubobjectDataBlueprintFunctionLibrary.get_data(subhandle)component = unreal.SubobjectDataBlueprintFunctionLibrary.get_object_for_blueprint(subdata, blueprint)component_name = unreal.SubobjectDataBlueprintFunctionLibrary.get_variable_name(subdata)unreal.log(“Component: “” + component.get_class().get_name() + “” Name: “” + component_name.str() + “””)

        unreal.log(“”)`Once you have a handle to a subobject, you can use the SubobjectDataBlueprintFunctionLibrary to get its internal SubobjectData:

        subdata = unreal.SubobjectDataBlueprintFunctionLibrary.get_data(subhandle)From there, you can query information about the subobject. Some examples:

        unreal.SubobjectDataBlueprintFunctionLibrary.is_component(subdata) unreal.SubobjectDataBlueprintFunctionLibrary.is_root_component(subdata) unreal.SubobjectDataBlueprintFunctionLibrary.is_scene_component(subdata) unreal.SubobjectDataBlueprintFunctionLibrary.is_native_component(subdata) unreal.SubobjectDataBlueprintFunctionLibrary.is_inherited_component(subdata) unreal.SubobjectDataBlueprintFunctionLibrary.get_variable_name(subdata)You can also access the component’s object and set variables on it directly:

        `# Get the component in the blueprint where it was definedcomponent = unreal.SubobjectDataBlueprintFunctionLibrary.get_object(subdata)

        Get the component in the “blueprint” object, where inherited components can override variables from their parent

        component = unreal.SubobjectDataBlueprintFunctionLibrary.get_object_for_blueprint(subdata, blueprint)

        if component.get_class().get_name() == “StaticMeshComponent”:static_mesh = unreal.StaticMeshComponent.cast(component)static_mesh.set_editor_property(“visible”, True)`Note that there are two functions to get the component object. Consider you have a hierarchy like the following:

        `- BPActor1 containing BPComponent1

        BPActor2 containing BPComponent2

        BPActor3 containing BPComponent3`In that hierarchy, BPActor3 defines BPComponent3 and inherits all the components from their ancestors. Here are some example gets:

        `get_object(BPComponent1Data) → returns BPComponent1 on BPActor1get_object(BPComponent2Data) → returns BPComponent2 on BPActor2get_object(BPComponent3Data) → returns BPComponent3 on BPActor3

        get_object_for_blueprint(BPComponent1Data, BPActor1) → returns BPComponent1 on BPActor1get_object_for_blueprint(BPComponent1Data, BPActor2) → returns BPComponent1’s override on BPActor2get_object_for_blueprint(BPComponent1Data, BPActor3) → returns BPComponent1’s override on BPActor3get_object_for_blueprint(BPComponent2Data, BPActor2) → returns BPComponent2 on BPActor2get_object_for_blueprint(BPComponent2Data, BPActor3) → returns BPComponent2’s override on BPActor3get_object_for_blueprint(BPComponent3Data, BPActor3) → returns BPComponent3 on BPActor3`I hope this is helpful. Please let me know if this solution works for you, or if you still need any further assistance.

        Best regards,

        Vitor

    