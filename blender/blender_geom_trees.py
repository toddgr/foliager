"""
File name: blender_place_trees.py
Author: Grace Todd
Date: September 24, 2024
Description: This file uses Blender Geometry nodes and particle systems to generate tree
            assets based on the input dimensions of a tree.
"""

import bpy
#import bmesh

def verify_units_metric():
    # Get the current scene unit system
    scene = bpy.context.scene
    unit_settings = scene.unit_settings

    # Check if the unit system is set to 'METRIC'
    if unit_settings.system != 'METRIC':
        print("Warning: Unit system is not set to Metric. Setting it to Metric now.")
        unit_settings.system = 'METRIC'
    else:
        print("Metric units are already in use.")

def create_tree_mesh(name):
    # Make sure that everything is in meters
    verify_units_metric()

    # Define the vertices
    vertices = [(0, 0, 0), (0, 0, 20)]
    
    # Define edges (a line connecting the two vertices)
    edges = [(0, 1)]
    
    # No faces since it's just a line
    faces = []

    # Create a new mesh and object
    mesh = bpy.data.meshes.new(name=name+"_mesh")
    obj = bpy.data.objects.new(name, mesh)

    # Link the object to the scene collection
    bpy.context.collection.objects.link(obj)

    # Create the mesh from the vertices/edges/faces
    mesh.from_pydata(vertices, edges, faces)

    # Update the mesh with new geometry
    mesh.update()

if __name__ == '__main__':
    create_tree_mesh("tree")