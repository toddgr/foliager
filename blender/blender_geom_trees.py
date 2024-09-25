"""
File name: blender_place_trees.py
Author: Grace Todd
Date: September 24, 2024
Description: This file uses Blender Geometry nodes and particle systems to generate tree
            assets based on the input dimensions of a tree.
"""

import bpy
#import bmesh

def create_node(node_tree, node_location, type_name):
    node_obj = node_tree.nodes.new(type=type_name)
    node_obj.location.x = node_location
    node_location += 300

    return node_obj, node_location

def link_nodes(node_tree, from_node, from_type, to_node, to_type):
    node_tree.links.new(from_node.outputs[from_type], to_node.inputs[to_type])

def create_geometry_node_tree(obj):
    bpy.ops.node.new_geometry_nodes_modifier()
    node_tree = bpy.data.node_groups["Geometry Nodes"]
    node_tree.name = "ScriptTesting"

    node_location = 0
    in_node = node_tree.nodes["Group Input"]
    in_node.location = (-300,0)
    

    # add a mesh to curve node
    mesh_to_curve, node_location = create_node(node_tree, node_location, "GeometryNodeMeshToCurve")
    link_nodes(node_tree, in_node, "Geometry", mesh_to_curve, "Mesh")
    
    curve_to_mesh, node_location = create_node(node_tree, node_location, "GeometryNodeCurveToMesh")
    link_nodes(node_tree, mesh_to_curve, "Curve", curve_to_mesh, "Curve")
    
    out_node = node_tree.nodes["Group Output"]
    out_node.location = (node_location, 0)
    link_nodes(node_tree, curve_to_mesh, "Mesh", out_node, "Geometry")


def init_tree_mesh(name, height):

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