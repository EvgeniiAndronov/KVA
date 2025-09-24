import os
import unittest

class TestCountLinesInFile(unittest.TestCase):
    
    def setUp(self):
        self.test_file = "line_test.txt"
    
    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_count_lines_with_content(self):
        from scan_module.read_files import count_lines_in_file
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("line1\nline2\nline3\n")
        
        count = count_lines_in_file(self.test_file)
        self.assertEqual(count, 3)
    
    def test_count_lines_empty_file(self):
        from scan_module.read_files import count_lines_in_file
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("")
        
        count = count_lines_in_file(self.test_file)
        self.assertEqual(count, 0)
    
    def test_count_lines_with_blank_lines(self):
        from scan_module.read_files import count_lines_in_file
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("line1\n\nline2\n  \nline3\n")
        
        count = count_lines_in_file(self.test_file)
        self.assertEqual(count, 3)

if __name__ == '__main__':
    unittest.main()