"""
File name: blender_place_trees.py
Author: Grace Todd
Date: September 24, 2024
Description: This file uses Blender Geometry nodes and particle systems to generate tree
            assets based on the input dimensions of a tree.
            create_node() and link_nodes() based on functions created by blender_plus_python:
            https://github.com/CGArtPython/blender_plus_python/blob/main/geo_nodes/subdivided_triangulated_cube

"""

import bpy
#import bmesh

DBH = 0.203 # diameter at breast height for now

SPACING = 250

def create_node(node_tree, node_location, type_name):
    node_obj = node_tree.nodes.new(type=type_name)
    node_obj.location.x = node_location
    node_location += SPACING

    return node_obj, node_location

def link_nodes(node_tree, from_node, from_type, to_node, to_type):
    node_tree.links.new(from_node.outputs[from_type], to_node.inputs[to_type])

def link_curve_nodes(node_tree, from_node, to_node):
    node_tree.links.new(from_node.outputs["Curve"], to_node.inputs["Curve"])

def create_geometry_node_tree():
    bpy.ops.node.new_geometry_nodes_modifier()
    node_tree = bpy.data.node_groups["Geometry Nodes"]
    node_tree.name = "ScriptTesting"

    node_location, curve_to_mesh = create_tree_base(node_tree)
    
    out_node = node_tree.nodes["Group Output"]
    out_node.location = (node_location, 0)
    link_nodes(node_tree, curve_to_mesh, "Mesh", out_node, "Geometry")

def create_tree_base(node_tree):
    """
    Create the base of the tree
    Input: Group Input
    Output: Curve to Mesh
    """
    node_x_location = 0
    node_y_location = 0


    in_node = node_tree.nodes["Group Input"]
    in_node.location = (-SPACING,0)
    
    # Create a Frame node
    frame_node = node_tree.nodes.new(type='NodeFrame')
    frame_node.label = "Create the tree trunk/base"
    frame_node.location = (node_x_location, node_y_location)  # Position the frame

    # mesh to curve
    mesh_to_curve, node_x_location = create_node(node_tree, node_x_location, "GeometryNodeMeshToCurve")
    link_nodes(node_tree, in_node, "Geometry", mesh_to_curve, "Mesh")
    mesh_to_curve.parent = frame_node

    # trim curve
    trim_curve, node_x_location = create_node(node_tree, node_x_location, "GeometryNodeTrimCurve")
    link_curve_nodes(node_tree, mesh_to_curve, trim_curve)
    trim_curve.parent = frame_node

    # resample curve
    resample_curve, node_x_location = create_node(node_tree, node_x_location, "GeometryNodeResampleCurve")
    link_curve_nodes(node_tree, trim_curve, resample_curve)
    resample_curve.parent = frame_node

    # set curve radius
    curve_circle_location = (node_x_location, node_y_location - (SPACING / 2))
    set_curve_radius, node_x_location = create_node(node_tree, node_x_location, "GeometryNodeSetCurveRadius")
    link_curve_nodes(node_tree, resample_curve, set_curve_radius)
    set_curve_radius.parent = frame_node

    #   set trunk thickness
    curve_radius = set_trunk_thickness(node_tree, DBH, node_x_location-(SPACING * 5), node_y_location + SPACING)
    link_nodes(node_tree, curve_radius, "Value", set_curve_radius, "Radius")

    # curve to mesh
    curve_to_mesh, node_x_location = create_node(node_tree, node_x_location, "GeometryNodeCurveToMesh")
    link_curve_nodes(node_tree, set_curve_radius, curve_to_mesh)
    curve_to_mesh.parent = frame_node

    #   curve circle
    curve_circle, node_x_location = create_node(node_tree, node_x_location, "GeometryNodeCurvePrimitiveCircle")
    curve_circle.location = curve_circle_location
    link_nodes(node_tree, curve_circle, "Curve", curve_to_mesh, "Profile Curve")
    curve_circle.parent = frame_node
    
    frame_node.width = (curve_to_mesh.location.x  - mesh_to_curve.location.x)  # Adjust width to fit nodes
    frame_node.height = (curve_circle.location.y  - mesh_to_curve.location.y) # Adjust height
    
    return node_x_location, curve_to_mesh

def set_trunk_thickness(node_tree, dbh, node_x_location, node_y_location):
    """
    Input: Diameter at breast height (m)
    Output: Radius value for Set Curve Radius
    """
    # Create a Frame node
    frame_node = node_tree.nodes.new(type='NodeFrame')
    frame_node.label = "Taper trunk / Scale to DBH"
    frame_node.location = (node_x_location, node_y_location)  # Position the frame

    # spline parameter
    spline_parameter, node_x_location = create_node(node_tree, node_x_location, "GeometryNodeSplineParameter")
    spline_parameter.location.y = node_y_location
    spline_parameter.parent = frame_node

    # float curve
    float_curve, node_x_location = create_node(node_tree, node_x_location, "ShaderNodeFloatCurve")
    float_curve.location.y = node_y_location + (SPACING / 2)
    link_nodes(node_tree, spline_parameter, "Factor", float_curve, "Value")
    float_curve.parent = frame_node

    # subtract from 1
    subtract_location = (node_x_location, node_y_location)
    subtract, node_x_location = create_node(node_tree, node_x_location, "ShaderNodeMath")
    subtract.operation = 'SUBTRACT'
    subtract.inputs[1].default_value = 1.0  # Set the second input to 1
    subtract.location = subtract_location
    link_nodes(node_tree, float_curve, "Value", subtract, "Value")
    subtract.parent = frame_node

    # multiply
    multiply, node_x_location = create_node(node_tree, node_x_location, "ShaderNodeMath")
    multiply.operation = 'MULTIPLY'
    multiply.inputs[1].default_value = dbh
    multiply.location.y = node_y_location
    link_nodes(node_tree, subtract, "Value", multiply, "Value")

    # get the group input

    # group output
    
    return multiply # a group


def make_tree_base():
    pass


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
    create_geometry_node_tree()

if __name__ == '__main__':
    create_tree_with_geometry_nodes("Douglas_Fir", 10)