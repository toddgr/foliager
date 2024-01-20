"""
File name: tree_class_test.py
Author: Grace Todd
Date: 2024-01-19
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
