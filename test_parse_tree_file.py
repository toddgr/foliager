import unittest
from tree_class import parse_tree_file, Tree

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

    def test_parse_tree_file_empty_file(self):
        with open(self.temp_file_path, 'w') as temp_file:
            temp_file.write("")

        result_trees = parse_tree_file(self.temp_file_path)

        self.assertEqual(result_trees, [])

    def test_parse_tree_file_invalid_format(self):
        with open(self.temp_file_path, 'w') as temp_file:
            temp_file.write("Oak\nPine\nInvalid Line\nBirch\n")

        result_trees = parse_tree_file(self.temp_file_path)

        self.assertEqual(result_trees, [])  # Expect an empty list due to the invalid line

    def test_parse_tree_file_file_not_found(self):
        result_trees = parse_tree_file("nonexistent_file.txt")

        self.assertEqual(result_trees, [])  # Expect an empty list for a non-existent file

if __name__ == '__main__':
    unittest.main()
