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
TOTAL_HEIGHT = 5
TRUNK_HEIGHT = TOTAL_HEIGHT / 3
CANOPY_DENSITY = 10
C_DIAM = 4
C_RADIUS = C_DIAM / 2
BRANCH_BEND = 0.1

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

    node_location, curve_to_mesh, resample_curve = create_tree_base(node_tree)
    node_location, instance_on_points = create_base_branches(node_tree)
    link_nodes(node_tree, resample_curve, "Curve", instance_on_points, "Points")

    # join geometry
    join_geometry, node_location = create_node(node_tree, node_location, "GeometryNodeJoinGeometry")
    link_nodes(node_tree, curve_to_mesh, "Mesh", join_geometry, "Geometry")
    link_nodes(node_tree, instance_on_points, "Instances", join_geometry, "Geometry")

    # realize instances
    realize_instances, node_location = create_node(node_tree, node_location, "GeometryNodeRealizeInstances")
    link_nodes(node_tree, join_geometry, "Geometry", realize_instances, "Geometry")

    
    out_node = node_tree.nodes["Group Output"]
    out_node.location = (node_location, 0)
    link_nodes(node_tree, realize_instances, "Geometry", out_node, "Geometry")

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
    resample_curve.inputs[2].default_value = CANOPY_DENSITY # Set the count to the density
    resample_curve.parent = frame_node
    
    # branch trimming

    # set curve radius
    curve_circle_location = (node_x_location, node_y_location - (SPACING / 2))
    set_curve_radius, node_x_location = create_node(node_tree, node_x_location, "GeometryNodeSetCurveRadius")
    link_curve_nodes(node_tree, resample_curve, set_curve_radius)
    set_curve_radius.parent = frame_node

    #   set trunk thickness
    curve_radius = set_thickness(node_tree, DBH, node_x_location-(SPACING * 5), node_y_location + (SPACING * 1.5), "Taper trunk / Scale to DBH", trunk=True)
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
    
    return node_x_location, curve_to_mesh, resample_curve

def set_thickness(node_tree, dbh, node_x_location, node_y_location, frame_label, trunk=False):
    """
    Input: Diameter at breast height (m)
    Output: Radius value for Set Curve Radius
    """
    # Create a Frame node
    frame_node = node_tree.nodes.new(type='NodeFrame')
    frame_node.label = frame_label
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

    if trunk:
        # multiply
        multiply, node_x_location = create_node(node_tree, node_x_location, "ShaderNodeMath")
        multiply.operation = 'MULTIPLY'
        multiply.inputs[1].default_value = dbh
        multiply.location.y = node_y_location
        link_nodes(node_tree, subtract, "Value", multiply, "Value")
        multiply.parent = frame_node

        frame_node.width = (multiply.location.x  - spline_parameter.location.x)  # Adjust width to fit nodes
        frame_node.height = (multiply.location.y  - float_curve.location.y) # Adjust height

        return multiply # links back to the tree base nodes
    
    frame_node.width = (subtract.location.x  - spline_parameter.location.x)  # Adjust width to fit nodes
    frame_node.height = (subtract.location.y  - float_curve.location.y) # Adjust height

    return subtract


def create_base_branches(node_tree):
    """
    Create the base of the tree
    Input: Group Input
    Output: Curve to Mesh
    """
    node_x_location = 0
    node_y_location = -SPACING * 3.5

    # Create a Frame node
    frame_node = node_tree.nodes.new(type='NodeFrame')
    frame_node.label = "Base Branch Generation"
    frame_node.location = (node_x_location, node_y_location-SPACING)  # Position the frame

    # curve line
    curve_line, node_x_location = create_node(node_tree, node_x_location, "GeometryNodeCurvePrimitiveLine")
    curve_line.location.y = node_y_location
    curve_line.mode = 'DIRECTION'
    curve_line.inputs[3].default_value = C_RADIUS + (C_RADIUS/4)
    curve_line.parent = frame_node

    # resample curve
    resample_curve, node_x_location = create_node(node_tree, node_x_location, "GeometryNodeResampleCurve")
    resample_curve.location.y = node_y_location
    link_curve_nodes(node_tree, curve_line, resample_curve)
    resample_curve.parent = frame_node
    
    # set position
    position = add_branch_curves(node_tree, node_x_location - (SPACING * 3), node_y_location - (SPACING))

    set_position, node_x_location = create_node(node_tree, node_x_location, "GeometryNodeSetPosition")
    set_position.location.y = node_y_location
    link_nodes(node_tree, resample_curve, "Curve", set_position, "Geometry")
    link_nodes(node_tree, position, "Vector", set_position, "Position")
    set_position.parent = frame_node

    # set curve radius
    curve_circle_location = (node_x_location, node_y_location - (SPACING / 2))
    set_curve_radius , node_x_location = create_node(node_tree, node_x_location, "GeometryNodeSetCurveRadius")
    set_curve_radius.location.y = node_y_location
    link_nodes(node_tree, set_position, "Geometry", set_curve_radius, "Curve")
    set_curve_radius.parent = frame_node

    # branch thickness  
    radius = set_thickness(node_tree, DBH, node_x_location - (SPACING*5), node_y_location + (SPACING * 1.5), "Taper branch")
    link_nodes(node_tree, radius, "Value", set_curve_radius, "Radius")
    
    # curve to mesh
    curve_to_mesh, node_x_location = create_node(node_tree, node_x_location, "GeometryNodeCurveToMesh")
    curve_to_mesh.location.y = node_y_location
    link_curve_nodes(node_tree, set_curve_radius, curve_to_mesh)
    curve_to_mesh.parent = frame_node
    
    # curve circle
    curve_circle, node_x_location = create_node(node_tree, node_x_location, "GeometryNodeCurvePrimitiveCircle")
    curve_circle.location = curve_circle_location
    curve_circle.inputs[4].default_value = 0.1 # branch radius needs to be small
    link_nodes(node_tree, curve_circle, "Curve", curve_to_mesh, "Profile Curve")
    curve_circle.parent = frame_node
    
    # map range for branch radius
    map_range_radius, node_x_location = create_node(node_tree, node_x_location, "ShaderNodeMapRange")
    map_range_radius.location.y = curve_circle_location[1]
    map_range_radius.location.x = curve_circle_location[0] + SPACING
    map_range_radius.clamp = True
    link_nodes(node_tree, radius, "Value", map_range_radius, "Value")
    # TODO make these values dynamic, will be affected by the C_DIAM
    # Could influence tree shape?
    map_range_radius.inputs[1].default_value = 0    # from min
    map_range_radius.inputs[2].default_value = 0 # from max
    map_range_radius.inputs[3].default_value = 1  # to min
    map_range_radius.inputs[4].default_value = 1  # to max
    map_range_radius.parent = frame_node

    # create the branches on the branches
    branch_level_two_instances = create_level_two_branches(node_tree, node_x_location, node_y_location, set_position)
    
    # join geometry
    #   create join geometry node
    #   link curve to mesh to it
    #   link bl2instances to it
    
    rotation = rotate_branches(node_tree, node_x_location, node_y_location)
    
    # instance on points
    instance_on_points, node_x_location = create_node(node_tree, node_x_location-SPACING, "GeometryNodeInstanceOnPoints")
    instance_on_points.location.y = node_y_location
    link_nodes(node_tree, curve_to_mesh, "Mesh", instance_on_points, "Instance")
    link_nodes(node_tree, map_range_radius, "Result", instance_on_points, "Scale")
    link_nodes(node_tree, rotation, "Rotation", instance_on_points, "Rotation")
    instance_on_points.parent = frame_node
    
    # branch trimming
    selection = trim_branches(node_tree, node_x_location, node_y_location)
    link_nodes(node_tree, selection, "Result", instance_on_points, "Selection")

    frame_node.width = (instance_on_points.location.x  - curve_line.location.x - SPACING)  # Adjust width to fit nodes
    frame_node.height = (curve_line.location.y  - SPACING) # Adjust height
    
    return node_x_location, instance_on_points

def add_branch_curves(node_tree, node_x_location, node_y_location):
    """
    Input: node tree, starting position
    Output: Position of the branch segment to be set
    """
    
    # index
    index, node_x_location = create_node(node_tree, node_x_location, "GeometryNodeInputIndex")
    index.location.y = node_y_location - SPACING
    
    # multiply
    multiply, node_x_location = create_node(node_tree, node_x_location, "ShaderNodeMath")
    multiply.operation = 'MULTIPLY'
    multiply.inputs[1].default_value = BRANCH_BEND
    multiply.location.y = node_y_location - SPACING
    link_nodes(node_tree, index, "Index", multiply, "Value")
    
    # position
    node_x_location -= SPACING
    position, node_x_location = create_node(node_tree, node_x_location, "GeometryNodeInputPosition")
    position.location.y = node_y_location - (SPACING/2)

    # vector rotate
    vector_rotate, node_x_location = create_node(node_tree, node_x_location, "ShaderNodeVectorRotate")
    vector_rotate.location.y = node_y_location
    vector_rotate.rotation_type = 'X_AXIS'
    link_nodes(node_tree, multiply, "Value", vector_rotate, "Angle")
    link_nodes(node_tree, position, "Position", vector_rotate, "Vector")

    return vector_rotate

def trim_branches(node_tree, node_x_location, node_y_location):
    node_x_location -= SPACING * 4
    node_y_location += SPACING * 2

    # Create a Frame node
    frame_node = node_tree.nodes.new(type='NodeFrame')
    frame_node.label = "Trim Branches"
    frame_node.location = (node_x_location, node_y_location-SPACING)  # Position the frame


    # subtract
    subtract, _ = create_node(node_tree, node_x_location, "ShaderNodeMath")
    subtract.operation = 'SUBTRACT'
    subtract.inputs[0].default_value = CANOPY_DENSITY - ((CANOPY_DENSITY/10) * 3)
    subtract.inputs[1].default_value = 1.0  # Set the second input to 1
    subtract.location.y = node_y_location

    # spline parameter
    spline_parameter, node_x_location = create_node(node_tree, node_x_location, "GeometryNodeSplineParameter")
    spline_parameter.location.y = node_y_location - SPACING
    spline_parameter.parent = frame_node

    # less than
    less_than, _ = create_node(node_tree, node_x_location, "FunctionNodeCompare")
    less_than.operation = 'LESS_THAN'
    less_than.location.y = node_y_location
    link_nodes(node_tree, spline_parameter, "Index", less_than, "A")
    link_nodes(node_tree, subtract, "Value", less_than, "B")
    less_than.parent = frame_node

    # greater than
    greater_than, node_x_location = create_node(node_tree, node_x_location, "FunctionNodeCompare")
    greater_than.operation = 'GREATER_THAN'
    greater_than.location.y = node_y_location - SPACING
    greater_than.inputs[1].default_value = TRUNK_HEIGHT
    link_nodes(node_tree, spline_parameter, "Index", greater_than, "A")
    greater_than.parent = frame_node

    # equal
    equal, _ = create_node(node_tree, node_x_location, "FunctionNodeCompare")
    equal.operation = 'EQUAL'
    equal.location.y = node_y_location
    link_nodes(node_tree, greater_than, "Result", equal, "A")
    link_nodes(node_tree, less_than, "Result", equal, "B")
    equal.parent = frame_node

    frame_node.width = (equal.location.x  - subtract.location.x - SPACING)  # Adjust width to fit nodes
    frame_node.height = (greater_than.location.y  - subtract.location.x) # Adjust height
    
    return equal

def rotate_branches(node_tree, node_x_location, node_y_location):
    node_x_location -= SPACING * 4
    node_y_location -= SPACING * 2

    # spline parameter
    spline_parameter, node_x_location = create_node(node_tree, node_x_location, "GeometryNodeSplineParameter")
    spline_parameter.location.y = node_y_location
    
    # map range
    map_range, _ = create_node(node_tree, node_x_location, "ShaderNodeMapRange")
    map_range.location.y = node_y_location
    map_range.clamp = True
    # TODO make these values dynamic
    map_range.inputs[1].default_value = 0    # from min
    map_range.inputs[2].default_value = 0 # from max
    map_range.inputs[3].default_value = 0  # to min
    map_range.inputs[4].default_value = 1  # to max
    link_nodes(node_tree, spline_parameter, "Length", map_range, "Value")
    
    # random value (0, 0, 0) -> (0, 0, 360)
    random_value, node_x_location = create_node(node_tree, node_x_location, "FunctionNodeRandomValue")
    random_value.location.y = node_y_location - SPACING
    random_value.data_type = 'FLOAT_VECTOR'
    random_value.inputs[1].default_value = (0, 0, 360) # set the max Z-axis rotation to 360

    # align euler to vector
    euler_to_vector, _ = create_node(node_tree, node_x_location, "FunctionNodeAlignEulerToVector")
    euler_to_vector.location.y = node_y_location
    euler_to_vector.axis = 'Y'
    link_nodes(node_tree, random_value, "Value", euler_to_vector, "Rotation")
    link_nodes(node_tree, map_range, "Result", euler_to_vector, "Factor")

    return euler_to_vector

def create_level_two_branches(node_tree, node_x_location, node_y_location, set_position):
    return None


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
    create_tree_with_geometry_nodes("Douglas_Fir", TOTAL_HEIGHT)