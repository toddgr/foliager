import unittest
from tree_class import Tree, TreeList
from parse_tree_input import parse_tree_file

class TestParseTreeFile(unittest.TestCase):
    def setUp(self):
        # Create a temporary file with sample tree data for testing
        self.temp_file_path = 'temp_trees.txt'
        with open(self.temp_file_path, 'w') as temp_file:
            temp_file.write("1. Oak\n2. Pine\n3. Maple\n4. Birch\n")

    def tearDown(self):
        # Remove the temporary file after testing
        import os
        os.remove(self.temp_file_path)

    def test_parse_tree_file_valid_input(self):
        expected_tree_names = ['Oak', 'Pine', 'Maple', 'Birch']

        result_tree_list = parse_tree_file(self.temp_file_path)

        self.assertIsInstance(result_tree_list, TreeList)
        self.assertEqual(result_tree_list.get_tree_names(), expected_tree_names)

    def test_parse_tree_file_empty_file(self):
        with open(self.temp_file_path, 'w') as temp_file:
            temp_file.write("")

        result_tree_list = parse_tree_file(self.temp_file_path)

        self.assertIsInstance(result_tree_list, TreeList)
        self.assertEqual(result_tree_list.get_tree_names(), [])

    def test_parse_tree_file_file_not_found(self):
        result_tree_list = parse_tree_file("nonexistent_file.txt")

        self.assertIsInstance(result_tree_list, TreeList)
        self.assertEqual(result_tree_list.get_tree_names(), [])  # Expect an empty list for a non-existent file

if __name__ == '__main__':
    unittest.main()
