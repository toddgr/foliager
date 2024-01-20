"""
File: tree_class.py
Author: Grace Todd
Date: January 19, 2024
Description: Tree class. Holds information on a given tree type, derives information on each tree by parsing an input file.
            Currently only derives name, but will be able to hold more attributes in the future.
"""

class Tree:
    def __init__(self, name, growth_rate, average_lifespan):
        self.name = name
        # Potential attributes:
        # Deciduous vs. coniferous
        # Leaf shape and arrangement
        # Bark Texture and Color
        # Form and Habit
            # Average
        # Flower Type and Structure
        # Fruit and seed characteristics
        # Growth rate (fast-growing, moderate-growing, slow-growing)
        self.growth_rate = growth_rate
        # Lifespan
        self.average_lifespan = average_lifespan
        # Climate tolerance
        # Soil preferences
        # Disease resistance
        # Fall coloration (interesting)
        # Root system
        # Wood density and hardness

    
class TreeList:
    def __init__(self):
        self.trees = []

    def add_tree(self, tree):
        self.trees.append(tree)

    def get_tree_names(self):
        return [tree.name for tree in self.trees]
