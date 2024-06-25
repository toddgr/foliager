"""
File: create_tree_obj.py
Author: Grace Todd
Date: June 25, 2024
Description: Generates the data for each tree object in Blender
             Takes in the tree data from 3PG, returns a class object to be
             parsed through in Blender to create the object
"""

class TreeNode:
    """ i.e. the branches """
    def __init__(self, start, end):
        self.start = start  # Tuple (x, y, z)
        self.end = end      # Tuple (x, y, z)
        self.children = []  # List of child nodes

    def add_child(self, child_node):
        self.children.append(child_node)

    def __repr__(self):
        return f"TreeNode(start={self.start}, end={self.end}, children={len(self.children)})"

class Tree:
    def __init__(self, root=None):
        self.root = root

    def add_node(self, parent, start, end):
        new_node = TreeNode(start, end)
        if parent:
            parent.add_child(new_node)
        return new_node

    def traverse(self, node=None):
        if node is None:
            node = self.root
        nodes = [node]
        for child in node.children:
            nodes.extend(self.traverse(child))
        return nodes
    

if __name__ == '__main__':
    # example usage
    trunk = TreeNode((0, 0, 0), (1, 1, 1))
    branch1 = TreeNode((1, 1, 1), (1, 2, 1))
    trunk.add_child(branch1)
    
    tree = Tree(trunk)
    print(tree.traverse())