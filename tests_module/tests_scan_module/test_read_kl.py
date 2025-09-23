import os
import unittest
import json
import sys
sys.path.append('../../scan_module')
from read_layout import read_kl

class TestReadKl(unittest.TestCase):
    
    def setUp(self):
        self.json_file = "test_layout.json"
        self.csv_file = "test_layout.csv"
        self.txt_file = "test_layout.txt"
        
        # Create test files
        with open(self.json_file, "w", encoding="utf-8") as f:
            json.dump({"a": 1, "b": 2}, f)
        
        with open(self.csv_file, "w", encoding="utf-8") as f:
            f.write("key,value\na,1\nb,2\n")
        
        with open(self.txt_file, "w", encoding="utf-8") as f:
            f.write("a:1\nb:2\n")
    
    def tearDown(self):
        for file in [self.json_file, self.csv_file, self.txt_file]:
            if os.path.exists(file):
                os.remove(file)
    
    def test_read_json_layout(self):
        layout = read_kl(self.json_file)
        self.assertEqual(layout, {"a": 1, "b": 2})
    
    def test_read_csv_layout(self):
        layout = read_kl(self.csv_file)
        self.assertEqual(layout, {"a": 1.0, "b": 2.0})
    
    def test_read_nonexistent_file(self):
        layout = read_kl("nonexistent.kl")
        self.assertIsNone(layout)

if __name__ == '__main__':
    unittest.main()