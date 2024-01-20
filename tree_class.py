"""
File name: tree_class.py
Author: Grace Todd
Date: January 19, 2024
Description: Tree class. Holds information on a given tree type, derives information on each tree by parsing an input file.
"""


class Tree:

	def __init__(self, name=None, growth_rate=None, average_lifespan=None):
		self.name = name
		self.growth_rate = growth_rate
		self.average_lifespan = average_lifespan

	def get_name(self):
		return self.name

	def get_growth_rate(self):
		return self.growth_rate

	def get_average_lifespan(self):
		return self.average_lifespan

	def get_tree_info(self):
		return self.name, self.growth_rate, self.average_lifespan, 

class TreeList:

	def __init__(self, tree_list=None):
		if tree_list is not None:
			self.trees = tree_list
		else:
			self.trees = []

	def add_trees(self, tree):
		self.trees.append(tree)

	def get_tree_names(self):
		return [tree.get_name() for tree in self.trees]

	def get_tree_growth_rates(self):
		return [[tree.get_tree_name(), tree.get_growth_rate()] for tree in self.trees]

	def get_tree_average_lifespans(self):
		return [[tree.get_tree_name(), tree.get_average_lifespan()] for tree in self.trees]

	def get_all_tree_info(self):
		return [tree.get_tree_info() for tree in self.trees]