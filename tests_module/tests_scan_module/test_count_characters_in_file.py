import os
import unittest
import sys
sys.path.append('../../scan_module')
from read_files import count_characters_in_file

class TestCountCharactersInFile(unittest.TestCase):
    
    def setUp(self):
        self.test_file = "char_test.txt"
    
    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_count_characters_ascii(self):
        content = "abcdefghij"
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write(content)
        
        count = count_characters_in_file(self.test_file)
        self.assertEqual(count, len(content))
    
    def test_count_characters_unicode(self):
        content = "абвгд€¥£"
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write(content)
        
        count = count_characters_in_file(self.test_file)
        self.assertEqual(count, len(content))
    
    def test_count_characters_empty_file(self):
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("")
        
        count = count_characters_in_file(self.test_file)
        self.assertEqual(count, 0)

if __name__ == '__main__':
    unittest.main()