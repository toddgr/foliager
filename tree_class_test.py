"""
File name: tree_class_test.py
Author: Grace Todd
Date: January 19, 2024
Description: Tree class. Holds information on a given tree type, derives information on each tree by parsing an input file.
"""
class Tree:

	def __init__(self, name, growth_rate, average_lifespan):
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
