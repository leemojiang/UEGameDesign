import unreal
from typing import Optional


class ComponentBuilder:
    def __init__(self):
        self.SDS = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
        self.BFL = unreal.SubobjectDataBlueprintFunctionLibrary

    def get_actor_root_handle(self, object: Optional[unreal.Blueprint | unreal.Actor]):
        handles = self._get_subobject_handles(object)
        if not handles:
            raise Exception("No subobject handles found.")

        h0 = handles[0]
        subdata = self.BFL.get_data(h0)
        if not self.BFL.is_actor(subdata):
            raise Exception("The first handle is not an actor.")
        return h0

    def add_component(
        self,
        parent_handler: unreal.SubobjectDataHandle,
        blueprint: unreal.Blueprint,
        new_class,
        name: str,
    ) -> (unreal.SubobjectDataHandle, unreal.Object):
        sub_handle, fail_reason = self.SDS.add_new_subobject(
            params=unreal.AddNewSubobjectParams(
                parent_handle=parent_handler,
                new_class=new_class,
                blueprint_context=blueprint,
            )
        )

        if not fail_reason.is_empty():
            raise Exception(
                f"ERROR from sub_object_subsystem.add_new_subobject: {fail_reason}"
            )

        self.SDS.rename_subobject(handle=sub_handle, new_name=unreal.Text(name))
        self.SDS.attach_subobject(
            owner_handle=parent_handler, child_to_add_handle=sub_handle
        )

        obj: unreal.Object = self._get_component_object(sub_handle, blueprint)
        return sub_handle, obj

    def get_component(
        self,
        blueprint: unreal.Blueprint,
        name: str,
        comp_type: Optional[unreal.Class] = None,
    ) -> (unreal.SubobjectDataHandle, unreal.Object):
        handles = self._get_subobject_handles(blueprint)
        result = []
        for h in handles:
            if self.BFL.is_handle_valid(h):
                subdata = self.BFL.get_data(h)
                var_name = self.BFL.get_variable_name(subdata)
                if var_name == name:
                    obj = self._get_component_object(h, blueprint)
                    if comp_type is None or isinstance(obj, comp_type):
                        print(
                            f"Component with name {name} and type {comp_type} found! "
                        )
                        result = [h, obj]
        if not result:
            print(f"Component with name {name} and type {comp_type} not found.")
            return None, None
        else:
            return (*result,)

    def get_components_of_type(
        self, blueprint: unreal.Blueprint, comp_type: unreal.Class
    ) -> list[(unreal.SubobjectDataHandle, unreal.Object)]:
        result = []
        handles = self._get_subobject_handles(blueprint)
        for h in handles:
            if self.BFL.is_handle_valid(h):
                subdata = self.BFL.get_data(h)
                obj = self._get_component_object(h, blueprint)
                if obj.get_class() == comp_type:
                    result.append((h, obj))
        return result

    def print_component_info_for_handle(self, h):
        if self.BFL.is_handle_valid(h):
            subdata = self.BFL.get_data(h)
            comp_obj = self.BFL.get_object(subdata)
            clsname = comp_obj.get_class().get_name()
            # obj = self.BFL.get_object_for_blueprint(subdata, blueprint)
            name = self.BFL.get_variable_name(subdata)
            print(f"Component Name: {name}, Object: {comp_obj}")

            is_component = self.BFL.is_component(subdata)
            is_root = self.BFL.is_root_component(subdata)
            is_scene = self.BFL.is_scene_component(subdata)
            is_native = self.BFL.is_native_component(subdata)
            is_inherited = self.BFL.is_inherited_component(subdata)
            print(
                f"   Is Component: {is_component}, Root Component: {is_root}, Scene Component: {is_scene}, Native Component: {is_native}, Inherited Component: {is_inherited} \n"
            )

        else:
            print("Invalid handle:", h)

    def _get_subobject_handles(self, object: Optional[unreal.Blueprint | unreal.Actor]):
        if isinstance(object, unreal.Actor):
            return self.SDS.k2_gather_subobject_data_for_instance(context=object)
        elif isinstance(object, unreal.Blueprint):
            return self.SDS.k2_gather_subobject_data_for_blueprint(context=object)
        else:
            raise Exception(f"Wrong type {type(object)}")

    def print_components_info(
        self, blueprint: Optional[unreal.Blueprint | unreal.Actor] = None
    ):  
        
        handles = self._get_subobject_handles(blueprint)
        if not handles:
            raise Exception("No handles found.")

        for h in handles:
            if self.BFL.is_handle_valid(h):
                subdata = self.BFL.get_data(h)
                comp_obj = self.BFL.get_object(subdata)
                clsname = comp_obj.get_class().get_name()
                # obj = self.BFL.get_object_for_blueprint(subdata, blueprint)
                name = self.BFL.get_variable_name(subdata)
                print(f"Component Name: {name}, Object: {comp_obj}")

                is_component = self.BFL.is_component(subdata)
                is_root = self.BFL.is_root_component(subdata)
                is_scene = self.BFL.is_scene_component(subdata)
                is_native = self.BFL.is_native_component(subdata)
                is_inherited = self.BFL.is_inherited_component(subdata)
                print(
                    f"   Is Component: {is_component}, Root Component: {is_root}, Scene Component: {is_scene}, Native Component: {is_native}, Inherited Component: {is_inherited} \n"
                )

            else:
                print("Invalid handle:", h)

    def _get_component_object(self, handle, actor):
        if self.BFL.is_handle_valid(handle):
            subdata = self.BFL.get_data(handle)
            obj = self.BFL.get_object_for_blueprint(subdata, actor)
            return obj


# bp = unreal.load_object(None, r"/Game/Game/Generated/BP_TestActor")
# builder = ComponentBuilder()
# # handles = builder._get_subobject_handles(bp)
# # builder.print_components_info(handles)

# root_handle = builder.get_actor_root_handle(bp)
# print("Root Handle Obtained.")
# cls = getattr(unreal, "ChaosWheeledVehicleMovementComponent", None)
# move_comp_handle, move_comp_obj = builder.get_component(bp, "VehicleMovementComponent", cls)

# root= builder.get_actor_root_handle(bp)
# h,_ = builder.add_component(root,bp,unreal.StaticMeshComponent,"TestStatisticMesh2")
# builder.add_component(h,bp,unreal.StaticMeshComponent,"TestStatisticMesh3")
