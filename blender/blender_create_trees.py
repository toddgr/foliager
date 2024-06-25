"""
File name: blender_create_trees.py
Author: Grace Todd
Date: June 25, 2024
Description: This file aims to test out tree object generation using cylinders and recursive branch creation.
"""

import bpy
import bmesh

if __name__ == '__main__':

    # Ensure we are in Object Mode
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    # Delete all existing objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    # Create a cylinder
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=32,          # Number of vertices for the circle (default is 32)
        radius=1,             # Radius of the cylinder
        depth=2,              # Depth of the cylinder
        location=(0, 0, 0)    # Location where the cylinder will be created
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

    # Optional: Adjust the cylinder properties
    cylinder.name = "TaperedCylinder"

    # Optional: Adjust the material properties
    mat = bpy.data.materials.new(name="CylinderMaterial")
    mat.diffuse_color = (0.545, 0.271, 0.075, 1)  # Brown color in 0-1 scale
    cylinder.data.materials.append(mat)
