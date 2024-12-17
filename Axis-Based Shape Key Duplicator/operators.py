import bpy
from .utils import check_conditions

class MESH_OT_add_condition(bpy.types.Operator):
    bl_idname = "mesh.add_condition"
    bl_label = "Add Condition"

    def execute(self, context):
        props = context.scene.shape_key_axis_props
        condition = props.conditions.add()
        condition.name = f"#{len(props.conditions)}"
        return {'FINISHED'}

class MESH_OT_remove_condition(bpy.types.Operator):
    bl_idname = "mesh.remove_condition"
    bl_label = "Remove Condition"

    def execute(self, context):
        props = context.scene.shape_key_axis_props
        idx = props.active_condition_index
        if props.conditions and 0 <= idx < len(props.conditions):
            props.conditions.remove(idx)
            props.active_condition_index = max(0, idx - 1)
            for i, condition in enumerate(props.conditions):
                condition.name = f"#{i + 1}"
        return {'FINISHED'}

class MESH_OT_create_shape_key_by_axis(bpy.types.Operator):
    bl_idname = "mesh.create_shape_key_by_axis"
    bl_label = "Create Shape Key by Axis"

    def execute(self, context):
        props = context.scene.shape_key_axis_props
        obj = context.active_object

        if not obj or obj.type != 'MESH' or not obj.data.shape_keys:
            self.report({'ERROR'}, "Please select a valid mesh with shape keys.")
            return {'CANCELLED'}

        from_shape_key = obj.data.shape_keys.key_blocks.get(props.source_shape_key)
        if not from_shape_key or not props.conditions:
            self.report({'ERROR'}, "Source shape key or conditions are invalid.")
            return {'CANCELLED'}

        new_shape_key = obj.shape_key_add(name=f"modified_{props.source_shape_key}")
        for i, vert in enumerate(obj.data.vertices):
            if check_conditions(from_shape_key.data[i].co, props.conditions):
                new_shape_key.data[i].co = from_shape_key.data[i].co

        self.report({'INFO'}, "New shape key created successfully.")
        return {'FINISHED'}