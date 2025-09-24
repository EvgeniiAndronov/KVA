import os
import unittest
import json
import csv

class TestSaveLayoutToFile(unittest.TestCase):
    
    def setUp(self):
        self.test_layout = {"a": 1.5, "b": 2.0, "c": 3.7}
        self.test_files = {
            "json": "test_output.json",
            "csv": "test_output.csv",
            "txt": "test_output.txt",
            "xml": "test_output.xml"
        }
    
    def tearDown(self):
        for file in self.test_files.values():
            if os.path.exists(file):
                os.remove(file)
    
    def test_save_json(self):
        from scan_module.read_layout import save_layout_to_file
        result = save_layout_to_file(self.test_layout, self.test_files["json"], "json")
        self.assertTrue(result)
        
        with open(self.test_files["json"], "r", encoding="utf-8") as f:
            content = json.load(f)
        
        self.assertEqual(content["layout"], self.test_layout)
    
    def test_save_csv(self):
        from scan_module.read_layout import save_layout_to_file
        result = save_layout_to_file(self.test_layout, self.test_files["csv"], "csv")
        self.assertTrue(result)
        
        with open(self.test_files["csv"], "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
        
        self.assertEqual(rows[0], ["symbol", "error"])
        self.assertEqual(len(rows), 4)  # header + 3 rows
    
    def test_save_txt(self):
        from scan_module.read_layout import save_layout_to_file
        result = save_layout_to_file(self.test_layout, self.test_files["txt"], "txt")
        self.assertTrue(result)
        
        with open(self.test_files["txt"], "r", encoding="utf-8") as f:
            content = f.read()
        
        self.assertIn("a:1.5", content)
        self.assertIn("# Keyboard Layout Configuration", content)

if __name__ == '__main__':
    unittest.main()