bl_info = {
    "name": "Axis-Based-Shape-Key-Duplicator",
    "author": "blancgoat",
    "version": (1, 0, 0),
    "blender": (4, 2, 4),
    "location": "View3D > Sidebar > Axis Shape",
    "description": "Creates a shape key with changes applied only to vertices that satisfy the specific axis condition.",
    "warning": "",
    "wiki_url": "https://github.com/blancgoat/Axis-Based-Shape-Key-Duplicator",
    "category": "Mesh",
}

import bpy
from .properties import ShapeKeyCondition, ShapeKeyAxisProperties
from .operators import MESH_OT_add_condition, MESH_OT_remove_condition, MESH_OT_create_shape_key_by_axis
from .ui import VIEW3D_UL_conditions, VIEW3D_PT_shape_key_axis_tools

classes = [
    ShapeKeyCondition,
    ShapeKeyAxisProperties,
    MESH_OT_add_condition,
    MESH_OT_remove_condition,
    MESH_OT_create_shape_key_by_axis,
    VIEW3D_UL_conditions,
    VIEW3D_PT_shape_key_axis_tools
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.shape_key_axis_props = bpy.props.PointerProperty(type=ShapeKeyAxisProperties)

def unregister():
    del bpy.types.Scene.shape_key_axis_props
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
