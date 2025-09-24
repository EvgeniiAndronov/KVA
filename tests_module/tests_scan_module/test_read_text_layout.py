import os
import unittest

class TestReadTextLayout(unittest.TestCase):
    
    def setUp(self):
        self.test_file = "test_text.txt"
    
    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_colon_separator(self):
        from scan_module.read_layout import _read_text_layout
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("a:1\nb:2\nc:3\n")
        
        result = _read_text_layout(self.test_file)
        self.assertEqual(result, {"a": 1.0, "b": 2.0, "c": 3.0})
    
    def test_equal_separator(self):
        from scan_module.read_layout import _read_text_layout
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("a=1\nb=2\nc=3\n")
        
        result = _read_text_layout(self.test_file)
        self.assertEqual(result, {"a": 1.0, "b": 2.0, "c": 3.0})
    
    def test_with_comments(self):
        from scan_module.read_layout import _read_text_layout
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("# This is a comment\na:1\n// Another comment\nb:2\n")
        
        result = _read_text_layout(self.test_file)
        self.assertEqual(result, {"a": 1.0, "b": 2.0})

if __name__ == '__main__':
    unittest.main()