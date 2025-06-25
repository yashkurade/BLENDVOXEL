==============================
BlendVoxel - Voxel Grid Generator
==============================

Author: YashK.
Version: 1.0
Blender Version: 3.6
Category: 3D View > Sidebar > BlendVoxel

DESCRIPTION:
------------
BlendVoxel is a voxel modeling workspace for Blender that provides an interactive 3D grid, brush-based voxel placement, layer-based editing, and powerful mesh voxelization tools. Ideal for prototyping stylized 3D voxel assets directly inside Blender.

INSTALLATION:
-------------
1. Extract the 'BlendVoxelMaster.zip' ZIP file.
1. Open Blender.
2. Go to Edit > Preferences > Add-ons.
3. Click "Install..." and select 'BlendVoxel.zip' ZIP file. (MAKE SURE YOU DONT SELECT 'BlendVoxelMaster.zip' ZIP FILE)
4. Enable "Voxel Grid Generator" from the list.
5. Access the tools in the 3D View Sidebar (press `N`), under the "BlendVoxel" tab.

FEATURES:
---------

🧱 GRID DISPLAY & LAYERS
------------------------
- Select your collection.
- Toggle "Show Grid Frame" to enable the voxel grid overlay.
- Set the master grid dimensions (X, Y, Z).
- Switch the working layer using "Current Layer".
- Choose layer orientation: XY, XZ, or YZ.

✏️ VOXEL PLACEMENT
-------------------
- Choose brush shape: Single, Square, or Circle.
- Adjust brush radius for Square/Circle mode.
- Click "Add Voxels" and drag to draw voxel cubes interactively.
- Click "Remove Voxels" to erase them.

🎭 VOXEL BASE OBJECT
---------------------
- The first placed voxel creates a hidden base cube called `VoxelBase`.
- All voxel cubes are instances of this base for performance and memory efficiency.

🔧 UTILITY TOOLS
----------------
1. **Make Voxels Editable**
   - Converts all selected voxel instances into real, editable mesh objects.

2. **Optimise Voxels**
   - Joins selected voxels and merges nearby vertices using a small merge distance.
   - Useful for cleaning up voxel geometry before export or sculpting.

🧊 VOXELIZE ANY MESH
---------------------
- Use "Voxelize Selected Object" to convert any mesh into voxel cubes.
- Works with the current grid dimensions and orientation.
- The "Sensitivity" slider controls how close voxels must be to the surface to count.

TIPS:
-----
- Use different layers or dedicated collections to build multi-part voxel models.
- Keep your voxel dimensions low for better performance.
- After voxelizing, use "Make Editable" and "Optimise" before export.

LICENSE:
--------
This addon is free to use and modify for personal use. Attribution is appreciated but not required.

Enjoy voxel modeling inside Blender!
