import bpy

class ShapeKeyCondition(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name", default="Condition")
    axis: bpy.props.EnumProperty(
        name="Axis",
        items=[('X', "X Axis", "X 축"), ('Y', "Y Axis", "Y 축"), ('Z', "Z Axis", "Z 축")],
        default='X'
    )
    operator: bpy.props.EnumProperty(
        name="Operator",
        items=[('>', ">", ">"), ('>=', ">=", ">="), ('==', "==", "=="), ('<', "<", "<"), ('<=', "<=", "<=")],
        default='>'
    )
    value: bpy.props.FloatProperty(name="Value", description="Local coordinates", default=0.0)

class ShapeKeyAxisProperties(bpy.types.PropertyGroup):
    source_shape_key: bpy.props.StringProperty(name="Source Shape Key")
    conditions: bpy.props.CollectionProperty(type=ShapeKeyCondition)
    active_condition_index: bpy.props.IntProperty(default=0)
