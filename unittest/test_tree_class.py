import unittest
from junk_drawer.tree_class import Tree

class TestTreeClassGenerator(unittest.TestCase):
    def test_tree_class_instantiated(self):
        # Tree class exists
        try:
            from tree_class_test import Tree  # Replace 'your_module' with the actual module name
            self.assertTrue(hasattr(Tree, '__class__'), "Tree class not found")
        except ImportError:
            self.fail("Module not found")

    def test_tree_class_init(self):
        # Tree class initializes properly
        tree = Tree("Pine")
        self.assertEqual(tree.name, "Pine")

    def test_tree_class_get_function(self):
        # Tree class has get functions
        tree = Tree("Oak")
        self.assertEqual(tree.get_name(), "Oak")

    def test_tree_class_get_all_info(self):
        # get_all_info shows all info
        tree = Tree(name="Redwood", growth_rate="Fast", average_lifespan="800 years")
        self.assertEqual(tree.get_tree_info(), (tree.name, tree.growth_rate, tree.average_lifespan))

if __name__ == '__main__':
    unittest.main()
