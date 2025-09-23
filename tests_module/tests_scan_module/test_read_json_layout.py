import os
import unittest
import json
import sys
sys.path.append('../../scan_module')
from read_layout import _read_json_layout

class TestReadJsonLayout(unittest.TestCase):
    
    def setUp(self):
        self.test_file = "test_json.json"
    
    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_direct_layout(self):
        layout_data = {"a": 1, "b": 2, "c": 3}
        with open(self.test_file, "w", encoding="utf-8") as f:
            json.dump(layout_data, f)
        
        result = _read_json_layout(self.test_file)
        self.assertEqual(result, layout_data)
    
    def test_nested_layout(self):
        layout_data = {"layout": {"a": 1, "b": 2}}
        with open(self.test_file, "w", encoding="utf-8") as f:
            json.dump(layout_data, f)
        
        result = _read_json_layout(self.test_file)
        self.assertEqual(result, {"a": 1, "b": 2})
    
    def test_invalid_json_format(self):
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("invalid json content")
        
        with self.assertRaises(ValueError):
            _read_json_layout(self.test_file)

if __name__ == '__main__':
    unittest.main()