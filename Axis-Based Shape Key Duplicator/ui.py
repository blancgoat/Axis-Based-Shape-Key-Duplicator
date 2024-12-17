import bpy

class VIEW3D_UL_conditions(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        row = layout.row(align=True)
        row.label(text=item.name, icon='DOT')
        row.prop(item, "axis", text="")
        row.prop(item, "operator", text="")
        row.prop(item, "value", text="")

class VIEW3D_PT_shape_key_axis_tools(bpy.types.Panel):
    bl_label = "Shape Key Axis Tools"
    bl_idname = "VIEW3D_PT_shape_key_axis_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Axis Shape'

    def draw(self, context):
        layout = self.layout
        props = context.scene.shape_key_axis_props
        obj = context.active_object

        if obj and obj.type == 'MESH' and obj.data.shape_keys:
            layout.prop_search(props, "source_shape_key", obj.data.shape_keys, "key_blocks")
            row = layout.row()
            row.template_list("VIEW3D_UL_conditions", "", props, "conditions", props, "active_condition_index")
            col = row.column()
            col.operator("mesh.add_condition", icon="ADD", text="")
            col.operator("mesh.remove_condition", icon="REMOVE", text="")
            layout.operator("mesh.create_shape_key_by_axis", text="Create Shape Key")
