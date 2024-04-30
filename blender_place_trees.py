"""
File name: blender_place_trees.py
Author: Grace Todd
Date: April 30, 2024
Description: This file aims to test out different scripts for the Blender API, so that I can hopefully 
            Use Blender to generate the different tree assets and host the forest
            Because I think that would be really cool
"""

import bpy
import bmesh

def create_forest_floor():
    FOREST_FLOOR_SCALE = 2

    # Create a new mesh data
    ff_mesh_data = bpy.data.meshes.new(name="MeshData")

    # Create a new bmesh
    ff_bmesh = bmesh.new()

    # Create the "forest floor"
    ff_verts = [(-FOREST_FLOOR_SCALE, -FOREST_FLOOR_SCALE, 0), (FOREST_FLOOR_SCALE, -FOREST_FLOOR_SCALE, 0),\
     (FOREST_FLOOR_SCALE, FOREST_FLOOR_SCALE, 0), (-FOREST_FLOOR_SCALE, FOREST_FLOOR_SCALE, 0)]
    for v in ff_verts:
        ff_bmesh.verts.new(v)

    # Create edges and faces
    ff_bmesh.faces.new(ff_bmesh.verts)

    # Update the bmesh
    ff_bmesh.to_mesh(ff_mesh_data)
    ff_bmesh.free()

    # Create a new mesh object
    forest_floor = bpy.data.objects.new("ForestFloor", ff_mesh_data)

    # Link the mesh object to the scene
    scene = bpy.context.scene
    scene.collection.objects.link(forest_floor)

    # Set the location of the forest floor
    forest_floor.location = (0, 0, 0)  # center at origin
