import unittest

class TestIsNumeric(unittest.TestCase):
    
    def test_integer_string(self):
        """
        Тест, который проверяет распознавание 
        целочисленных строк
        """
        from scan_module.read_layout import _is_numeric
        self.assertTrue(_is_numeric("123"))
        self.assertTrue(_is_numeric("-456"))
        self.assertTrue(_is_numeric("0"))
    
    def test_float_string(self):
        """
        Тест, который проверяет распознавание 
        строк с числами с плавающей точкой
        """
        from scan_module.read_layout import _is_numeric
        self.assertTrue(_is_numeric("123.45"))
        self.assertTrue(_is_numeric("-78.90"))
        self.assertTrue(_is_numeric("0.0"))
        self.assertTrue(_is_numeric(".5"))
        self.assertTrue(_is_numeric("3."))
    
    def test_scientific_notation(self):
        """
        Тест, который проверяет распознавание 
        научной нотации
        """
        from scan_module.read_layout import _is_numeric
        self.assertTrue(_is_numeric("1.23e-4"))
        self.assertTrue(_is_numeric("5e10"))
        self.assertTrue(_is_numeric("-2.5E+3"))
    
    def test_non_numeric_strings(self):
        """
        Тест, который проверяет отклонение 
        нечисловых строк
        """
        from scan_module.read_layout import _is_numeric
        self.assertFalse(_is_numeric("abc"))
        self.assertFalse(_is_numeric("123abc"))
        self.assertFalse(_is_numeric(""))
        self.assertFalse(_is_numeric(" "))
        self.assertFalse(_is_numeric("1,234"))  # comma not supported
        self.assertFalse(_is_numeric("12.34.56"))  # multiple decimals

if __name__ == '__main__':
    unittest.main()