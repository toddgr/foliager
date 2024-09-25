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

def create_geometry_node_tree(obj):
    bpy.ops.node.new_geometry_nodes_modifier()
    node_tree = bpy.data.node_groups["Geometry Nodes"]
    node_tree.name = "ScriptTesting"
    

def init_tree_mesh(name, height):
    # Make sure that everything is in meters
    verify_units_metric()

    # Define the vertices
    vertices = [(0, 0, 0), (0, 0, height)]
    
    # Define edges (a line connecting the two vertices)
    edges = [(0, 1)]
    
    # No faces since it's just a line
    faces = []

    # Create a new mesh and object
    mesh = bpy.data.meshes.new(name=name+"_mesh")
    obj = bpy.data.objects.new(name, mesh)

    # Link the object to the scene collection
    bpy.context.collection.objects.link(obj)

    # Set the new object as the active object
    bpy.context.view_layer.objects.active = obj

    # Create the mesh from the vertices/edges/faces
    mesh.from_pydata(vertices, edges, faces)

    # Update the mesh with new geometry
    mesh.update()

    return obj

def create_tree_with_geometry_nodes(name, height):
    # Create the mesh first
    obj = init_tree_mesh(name, height)

    # Create the geometry node tree
    create_geometry_node_tree(obj)

if __name__ == '__main__':
    create_tree_with_geometry_nodes("Douglas_Fir", 20)