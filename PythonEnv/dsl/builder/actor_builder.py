# dsl/builder/actor_builder.py
import unreal
from dsl.builder.component_builder import ComponentBuilder
from dsl.models.actor_model import ActorModel

class ActorBuilder:

    def build_actor(self, model):
        """
        ActorModel → UE Actor
        """
        world = unreal.EditorLevelLibrary.get_editor_world()
        actor_class = unreal.load_object(None, model.class_name)

        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            actor_class,
            unreal.Vector(0, 0, 0)
        )

        # transform
        if model.transform:
            actor.set_actor_location(unreal.Vector(*model.transform.location))

        builder = ComponentBuilder(actor, model.class_name)

        # NonSceneComponent
        for comp in model.components:
            builder.build_non_scene_component(comp)

        # SceneComponent
        for sc in model.children:
            builder.build_scene_component(sc, None)

        return actor
    

