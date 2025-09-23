import os
import unittest
import sys
sys.path.append('../../scan_module')
from read_files import get_text_from_file

class TestGetTextFromFile(unittest.TestCase):
    
    def setUp(self):
        self.small_file = "text_test.txt"
        self.content = "This is a test content.\nWith multiple lines.\nAnd some text."
        with open(self.small_file, "w", encoding="utf-8") as f:
            f.write(self.content)
    
    def tearDown(self):
        if os.path.exists(self.small_file):
            os.remove(self.small_file)
    
    def test_get_text_normal_case(self):
        text = get_text_from_file(self.small_file)
        self.assertEqual(text, self.content)
    
    def test_get_text_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            get_text_from_file("nonexistent.txt")
    
    def test_get_text_encoding_fallback(self):
        text = get_text_from_file(self.small_file)
        self.assertIn("test content", text)

if __name__ == '__main__':
    unittest.main()