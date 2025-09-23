import unittest
import sys
sys.path.append('../../scan_module')
from read_layout import _is_numeric

class TestIsNumeric(unittest.TestCase):
    
    def test_integer_string(self):
        self.assertTrue(_is_numeric("123"))
        self.assertTrue(_is_numeric("-456"))
        self.assertTrue(_is_numeric("0"))
    
    def test_float_string(self):
        self.assertTrue(_is_numeric("123.45"))
        self.assertTrue(_is_numeric("-78.90"))
        self.assertTrue(_is_numeric("0.0"))
        self.assertTrue(_is_numeric(".5"))
        self.assertTrue(_is_numeric("3."))
    
    def test_scientific_notation(self):
        self.assertTrue(_is_numeric("1.23e-4"))
        self.assertTrue(_is_numeric("5e10"))
        self.assertTrue(_is_numeric("-2.5E+3"))
    
    def test_non_numeric_strings(self):
        self.assertFalse(_is_numeric("abc"))
        self.assertFalse(_is_numeric("123abc"))
        self.assertFalse(_is_numeric(""))
        self.assertFalse(_is_numeric(" "))
        self.assertFalse(_is_numeric("1,234"))  # comma not supported
        self.assertFalse(_is_numeric("12.34.56"))  # multiple decimals
    
    def test_boolean_strings(self):
        self.assertFalse(_is_numeric("True"))
        self.assertFalse(_is_numeric("False"))
    
    def test_none_value(self):
        self.assertFalse(_is_numeric("None"))

if __name__ == '__main__':
    unittest.main()