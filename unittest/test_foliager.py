import unittest
from foliager import make_valid_filename

class TestValidFilenames(unittest.TestCase):
    def test_make_valid_filename_basic(self):
        input_string = "Hello, World! File_Name123"
        result = make_valid_filename(input_string)
        self.assertEqual(result, "Hello_World_File_Name123_foliage.txt", "Basic test failed")

    def test_make_valid_filename_empty(self):
        input_string = ""
        result = make_valid_filename(input_string)
        self.assertEqual(result, "untitled_foliage.txt", "Empty string test failed")

    def test_make_valid_filename_special_characters(self):
        input_string = "@#$%^&*()_+"
        result = make_valid_filename(input_string)
        self.assertEqual(result, "untitled_foliage.txt", "Special characters test failed")

    def test_make_valid_filename_long_name(self):
        input_string = "a" * 300
        result = make_valid_filename(input_string)
        self.assertEqual(len(result), 255, "Long name test failed")

if __name__ == '__main__':
    unittest.main()