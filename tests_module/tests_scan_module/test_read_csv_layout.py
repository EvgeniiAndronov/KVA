import os
import unittest

class TestReadCsvLayout(unittest.TestCase):
    
    def setUp(self):
        self.test_file = "test_csv.csv"
    
    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_comma_delimited(self):
        from scan_module.read_layout import _read_csv_layout
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("a,1\nb,2\nc,3\n")
        
        result = _read_csv_layout(self.test_file)
        self.assertEqual(result, {"a": 1.0, "b": 2.0, "c": 3.0})
    
    def test_semicolon_delimited(self):
        from scan_module.read_layout import _read_csv_layout
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("a;1\nb;2\nc;3\n")
        
        result = _read_csv_layout(self.test_file)
        self.assertEqual(result, {"a": 1.0, "b": 2.0, "c": 3.0})
    
    def test_with_header(self):
        from scan_module.read_layout import _read_csv_layout
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("symbol,error\na,1\nb,2\n")
        
        result = _read_csv_layout(self.test_file)
        self.assertEqual(result, {"a": 1.0, "b": 2.0})

if __name__ == '__main__':
    unittest.main()