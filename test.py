bl_info = {
    "name": "Voxel Grid Generator",
    "author": "YashK.",
    "version": (0, 1),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar > VoxelArt",
    "description": "Voxel modeling workspace with grid, layer, and voxel placement",
    "category": "3D View",
}

import bpy
from bpy.props import BoolProperty, IntProperty, PointerProperty
from mathutils import Vector
from bpy_extras import view3d_utils


# ---------------------------- GRID FRAME ----------------------------------

def create_outline_cube(name, size_x, size_y, size_z, location=(0, 0, 0)):
    verts = [
        Vector((0, 0, 0)),
        Vector((size_x, 0, 0)),
        Vector((size_x, size_y, 0)),
        Vector((0, size_y, 0)),
        Vector((0, 0, size_z)),
        Vector((size_x, 0, size_z)),
        Vector((size_x, size_y, size_z)),
        Vector((0, size_y, size_z)),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7),
    ]

    mesh = bpy.data.meshes.new(name + "_mesh")
    mesh.from_pydata(verts, edges, [])
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    obj.display_type = 'WIRE'
    obj.hide_select = True
    obj.name = name
    return obj


def update_grid(context):
    props = context.scene.voxel_grid_props

    for name in ["VoxelGridMaster", "VoxelGridLayer"]:
        obj = bpy.data.objects.get(name)
        if obj:
            bpy.data.objects.remove(obj, do_unlink=True)

    if props.show_grid:
        create_outline_cube("VoxelGridMaster", props.dim_x, props.dim_y, props.dim_z)
        if 0 <= props.current_layer < props.dim_z:
            create_outline_cube("VoxelGridLayer", props.dim_x, props.dim_y, 1, location=(0, 0, props.current_layer))


# ---------------------------- PROPERTIES ----------------------------------

class VoxelGridProps(bpy.types.PropertyGroup):
    show_grid: BoolProperty(
        name="Show Grid Frame",
        default=False,
        update=lambda self, context: update_grid(context)
    )
    dim_x: IntProperty(name="X", default=5, min=1)
    dim_y: IntProperty(name="Y", default=5, min=1)
    dim_z: IntProperty(name="Z", default=5, min=1)
    current_layer: IntProperty(name="Z Layer", default=0, min=0)


# --------------------------- UI PANEL -------------------------------------

class VoxelGridPanel(bpy.types.Panel):
    bl_label = "Voxel Grid"
    bl_idname = "VIEW3D_PT_voxel_grid"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "VoxelArt"

    def draw(self, context):
        layout = self.layout
        props = context.scene.voxel_grid_props

        layout.prop(props, "show_grid")
        layout.prop(props, "dim_x")
        layout.prop(props, "dim_y")
        layout.prop(props, "dim_z")
        layout.prop(props, "current_layer")
        layout.operator("voxel.place_voxel", text="Start Placing Voxels")


# ---------------------- VOXEL PLACEMENT TOOL ------------------------------

class VOXEL_OT_place_voxel(bpy.types.Operator):
    """Click inside current Z-layer to add cubes"""
    bl_idname = "voxel.place_voxel"
    bl_label = "Place Voxels"
    bl_options = {'REGISTER'}

    def modal(self, context, event):
        if event.type in {'ESC', 'RIGHTMOUSE'}:
            self.report({'INFO'}, "Placement cancelled")
            return {'CANCELLED'}

        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            region = context.region
            rv3d = context.region_data
            coord = event.mouse_region_x, event.mouse_region_y

            view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
            ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)

            # Cast to the current Z layer
            props = context.scene.voxel_grid_props
            z_layer = props.current_layer
            plane_normal = Vector((0, 0, 1))
            plane_point = Vector((0, 0, z_layer))

            dot = view_vector.dot(plane_normal)
            if abs(dot) < 1e-5:
                return {'PASS_THROUGH'}

            t = (plane_point - ray_origin).dot(plane_normal) / dot
            hit_point = ray_origin + view_vector * t

            x = int(hit_point.x)
            y = int(hit_point.y)
            z = z_layer

            if 0 <= x < props.dim_x and 0 <= y < props.dim_y:
                self.add_voxel(x, y, z)

        return {'RUNNING_MODAL'}

    def add_voxel(self, x, y, z):
        size = 1
        pos = Vector((x + 0.5, y + 0.5, z + 0.5))
        name = f"voxel_{x}_{y}_{z}"
        if name not in bpy.data.objects:
            bpy.ops.mesh.primitive_cube_add(size=size, location=pos)
            obj = bpy.context.active_object
            obj.name = name

    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)
        self.report({'INFO'}, "Click in viewport to add voxels | ESC to cancel")
        return {'RUNNING_MODAL'}



# ------------------------- REGISTER ---------------------------------------

classes = [VoxelGridProps, VoxelGridPanel, VOXEL_OT_place_voxel]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.voxel_grid_props = PointerProperty(type=VoxelGridProps)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.voxel_grid_props

if __name__ == "__main__":
    register()
