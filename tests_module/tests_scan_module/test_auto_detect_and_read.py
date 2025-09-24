import os
import unittest
import json

class TestAutoDetectAndRead(unittest.TestCase):
    
    def setUp(self):
        self.test_files = {
            "json": "test_json.json",
            "csv": "test_csv.csv",
            "txt": "test_txt.txt"
        }
    
    def tearDown(self):
        for file in self.test_files.values():
            if os.path.exists(file):
                os.remove(file)
    
    def test_detect_json(self):
        from scan_module.read_layout import _auto_detect_and_read
        with open(self.test_files["json"], "w", encoding="utf-8") as f:
            json.dump({"a": 1, "b": 2}, f)
        
        result = _auto_detect_and_read(self.test_files["json"])
        self.assertEqual(result, {"a": 1, "b": 2})
    
    def test_detect_csv(self):
        from scan_module.read_layout import _auto_detect_and_read
        with open(self.test_files["csv"], "w", encoding="utf-8") as f:
            f.write("a,1\nb,2\n")
        
        result = _auto_detect_and_read(self.test_files["csv"])
        self.assertEqual(result, {"a": 1.0, "b": 2.0})
    
    def test_detect_text_fallback(self):
        from scan_module.read_layout import _auto_detect_and_read
        with open(self.test_files["txt"], "w", encoding="utf-8") as f:
            f.write("a:1\nb:2\n")
        
        result = _auto_detect_and_read(self.test_files["txt"])
        self.assertEqual(result, {"a": 1.0, "b": 2.0})

if __name__ == '__main__':
    unittest.main()