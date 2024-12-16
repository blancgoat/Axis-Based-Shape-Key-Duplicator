bl_info = {
    "name": "Axis-Based-Shape-Key-Duplicator",
    "author": "blancgoat",
    "version": (1, 0, 0),
    "blender": (4, 2, 4),
    "location": "View3D > Sidebar > Axis Shape",
    "description": "Creates a shape key with changes applied only to vertices that satisfy the specific axis condition.",
    "warning": "",
    "wiki_url": "github.com/blancgoat",
    "category": "Mesh",
}

import bpy
from bpy.props import StringProperty, EnumProperty, FloatProperty, CollectionProperty, PointerProperty
from bpy.types import Operator, Panel, PropertyGroup, UIList

class ShapeKeyCondition(PropertyGroup):
    name: StringProperty(
        name="Name",
        default="Condition"
    )

    axis: EnumProperty(
        name="Axis",
        items=[
            ('X', "X Axis", "X 축"),
            ('Y', "Y Axis", "Y 축"),
            ('Z', "Z Axis", "Z 축")
        ],
        default='X'
    )
    
    operator: EnumProperty(
        name="Operator",
        items=[
            ('>', ">", ">"),
            ('>=', ">=", ">="),
            ('==', "==", "=="),
            ('<', "<", "<"),
            ('<=', "<=", "<="),
        ],
        default='>'
    )

    value: FloatProperty(
        name="Value",
        description="Based on local coordinates (not global)",
        default=0.0
    )

class ShapeKeyAxisProperties(PropertyGroup):
    source_shape_key: StringProperty(
        name="Source Shape Key",
    )

    conditions: CollectionProperty(type=ShapeKeyCondition)
    active_condition_index: bpy.props.IntProperty(default=0)

class MESH_OT_add_condition(Operator):
    bl_idname = "mesh.add_condition"
    bl_label = "Add Condition"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.shape_key_axis_props
        condition = props.conditions.add()
        condition.name = f"#{len(props.conditions)}"
        return {'FINISHED'}

class MESH_OT_remove_condition(Operator):
    bl_idname = "mesh.remove_condition"
    bl_label = "Remove Condition"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.shape_key_axis_props
        idx = props.active_condition_index
        if props.conditions and 0 <= idx < len(props.conditions):
            props.conditions.remove(idx)
            props.active_condition_index = max(0, idx - 1)
            # 이름 재정렬
            for i, condition in enumerate(props.conditions):
                condition.name = f"#{i + 1}"
        else:
            self.report({'WARNING'}, "There are no conditions to delete.")
        return {'FINISHED'}

class MESH_OT_create_shape_key_by_axis(Operator):
    bl_idname = "mesh.create_shape_key_by_axis"
    bl_label = "Create Shape Key by Axis"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.shape_key_axis_props
        obj = context.active_object

        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "Please select a mesh object.")
            return {'CANCELLED'}

        if not obj.data.shape_keys:
            self.report({'ERROR'}, "This mesh does not have a shape key.")
            return {'CANCELLED'}

        if not props.conditions:
            self.report({'ERROR'}, "Please add a condition.")
            return {'CANCELLED'}

        try:
            from_shape_key = obj.data.shape_keys.key_blocks.get(props.source_shape_key)
            if not from_shape_key:
                self.report({'ERROR'}, "Please select a valid source shape key")
                return {'CANCELLED'}

            new_shape_key_name = f"modified_{props.source_shape_key}"
            new_shape_key = obj.shape_key_add(name=new_shape_key_name)
            new_shape_key.value = 0.0

            for i, vert in enumerate(obj.data.vertices):
                original_vert = from_shape_key.data[i].co

                if self.check_conditions(original_vert, props.conditions):
                    new_shape_key.data[i].co = original_vert

            self.report({'INFO'}, f"New shape key '{new_shape_key_name}' created successfully.")
            return {'FINISHED'}
        
        except Exception as e:
            self.report({'ERROR'}, f"Error occurred: {str(e)}")
            return {'CANCELLED'}

    def check_conditions(self, coord, conditions):
        for condition in conditions:
            value = getattr(coord, condition.axis.lower())
            if not eval(f"{value} {condition.operator} {condition.value}"):
                return False
        return True

class VIEW3D_UL_conditions(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            row.label(text=item.name, icon='DOT')  # 조건 이름 표시
            row.prop(item, "axis", text="")
            row.prop(item, "operator", text="")
            row.prop(item, "value", text="")
        elif self.layout_type == 'GRID':
            pass

class VIEW3D_PT_shape_key_axis_tools(Panel):
    bl_label = "Shape Key Axis Tools"
    bl_idname = "VIEW3D_PT_shape_key_axis_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Axis Shape'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.shape_key_axis_props

        obj = context.active_object
        if obj and obj.type == 'MESH' and obj.data.shape_keys:
            layout.prop_search(props, "source_shape_key", obj.data.shape_keys, "key_blocks")

            row = layout.row()
            row.label(text="Conditions:")
            row.template_list(
                "VIEW3D_UL_conditions",  # 리스트 클래스
                "",                      # 리스트 ID
                props,                   # 데이터 블록
                "conditions",            # 조건 컬렉션
                props,                   # 액티브 데이터
                "active_condition_index",  # 활성 인덱스
                rows=3
            )

            col = row.column(align=True)
            col.operator("mesh.add_condition", icon="ADD", text="")
            col.operator("mesh.remove_condition", icon="REMOVE", text="")

            layout.operator("mesh.create_shape_key_by_axis", text="Create Shape Key")
        else:
            layout.label(text="Please select a mesh object.")

def register():
    bpy.utils.register_class(ShapeKeyCondition)
    bpy.utils.register_class(ShapeKeyAxisProperties)
    bpy.utils.register_class(MESH_OT_add_condition)
    bpy.utils.register_class(MESH_OT_remove_condition)
    bpy.utils.register_class(MESH_OT_create_shape_key_by_axis)
    bpy.utils.register_class(VIEW3D_UL_conditions)
    bpy.utils.register_class(VIEW3D_PT_shape_key_axis_tools)

    bpy.types.Scene.shape_key_axis_props = PointerProperty(type=ShapeKeyAxisProperties)

def unregister():
    bpy.utils.unregister_class(ShapeKeyCondition)
    bpy.utils.unregister_class(ShapeKeyAxisProperties)
    bpy.utils.unregister_class(MESH_OT_add_condition)
    bpy.utils.unregister_class(MESH_OT_remove_condition)
    bpy.utils.unregister_class(MESH_OT_create_shape_key_by_axis)
    bpy.utils.unregister_class(VIEW3D_UL_conditions)
    bpy.utils.unregister_class(VIEW3D_PT_shape_key_axis_tools)

    del bpy.types.Scene.shape_key_axis_props

if __name__ == "__main__":
    register()
