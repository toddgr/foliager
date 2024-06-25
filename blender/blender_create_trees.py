"""
File name: blender_create_trees.py
Author: Grace Todd
Date: June 25, 2024
Description: This file aims to test out tree object generation using cylinders and recursive branch creation.
"""

import bpy

if __name__ == '__main__':
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

    # Optional: Adjust the cylinder properties
    cylinder = bpy.context.object
    cylinder.name = "MyCylinder"

    # Optional: Adjust the material properties
    mat = bpy.data.materials.new(name="CylinderMaterial")
    mat.diffuse_color = (0.545, 0.271, 0.075, 1)  # Brown color
    cylinder.data.materials.append(mat)