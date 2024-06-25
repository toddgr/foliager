"""
File name: blender_create_trees.py
Author: Grace Todd
Date: June 25, 2024
Description: This file aims to test out tree object generation using cylinders and recursive branch creation.
"""

import bpy
import bmesh

def silly_little_cylinder():
    # Ensure we are in Object Mode
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    # Delete all existing objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    # Create a cylinder
    depth = 8
    
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16,          # Number of vertices for the circle (default is 32)
        radius=1,             # Radius of the cylinder
        depth=depth,              # Depth of the cylinder
        location=(0, 0, depth/2)    # Location where the cylinder will be created -- Sets the bottom at the origin
    )

    # Get the cylinder object
    cylinder = bpy.context.object

    # Enter edit mode
    bpy.ops.object.mode_set(mode='EDIT')

    # Get the BMesh representation of the cylinder
    bm = bmesh.from_edit_mesh(cylinder.data)

    # Select the top vertices
    top_vertices = [v for v in bm.verts if v.co.z > 0.99]

    # Scale the top vertices
    bmesh.ops.scale(
        bm,
        vec=(0.5, 0.5, 0.5),  # Scale factor (smaller radius at the top)
        verts=top_vertices
    )

    # Update the mesh and exit edit mode
    bmesh.update_edit_mesh(cylinder.data)
    bpy.ops.object.mode_set(mode='OBJECT')

    # Rotate the cylinder around the new origin (bottom)
    cylinder.rotation_euler[0] += 0.2  # Rotate around X-axis
    cylinder.rotation_euler[1] += 0.1  # Rotate around Y-axis
    cylinder.rotation_euler[2] += 0.0  # Rotate around Z-axis (optional)

    # Optional: Adjust the cylinder properties
    cylinder.name = "TaperedCylinder"

    # Optional: Adjust the material properties
    mat = bpy.data.materials.new(name="CylinderMaterial")
    mat.diffuse_color = (0.545, 0.271, 0.075, 1)  # Brown color in 0-1 scale
    cylinder.data.materials.append(mat)

    

if __name__ == '__main__':
    # example usage
    silly_little_cylinder()
    
    
    # pseudocode for how we're gonna do this for every tree
    # 1. read in the OUTPUT_DATA.csv
    # for each tree_key
        # for each t interval