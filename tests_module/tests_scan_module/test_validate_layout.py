import unittest

class TestValidateLayout(unittest.TestCase):
    
    def test_valid_layout_full_alphabet(self):
        from scan_module.read_layout import validate_layout
        # Полный алфавит - должен проходить валидацию
        layout = {}
        for i in range(97, 123):  # a-z
            layout[chr(i)] = 1.0
        
        is_valid, errors = validate_layout(layout)
        self.assertTrue(is_valid, f"Validation failed with errors: {errors}")
        self.assertEqual(len(errors), 0)
    
    def test_valid_layout_adequate_chars(self):
        from scan_module.read_layout import validate_layout
        # Layout с достаточным количеством символов (больше чем 26-10=16)
        layout = {}
        # Добавляем 20 символов (a-t)
        for i in range(97, 117):  # a-t
            layout[chr(i)] = 1.0
        
        is_valid, errors = validate_layout(layout)
        self.assertTrue(is_valid, f"Validation failed with errors: {errors}")
        self.assertEqual(len(errors), 0)
    
    def test_invalid_layout_too_few_chars(self):
        from scan_module.read_layout import validate_layout
        # Layout с слишком малым количеством символов (меньше 16)
        layout = {"a": 1, "b": 2, "c": 3}  # только 3 символа
        
        is_valid, errors = validate_layout(layout)
        self.assertFalse(is_valid)
        # Должна быть ошибка про отсутствующие символы
        missing_errors = [e for e in errors if "Отсутствуют" in e or "базовые" in e]
        self.assertGreater(len(missing_errors), 0)
    
    def test_invalid_key_type(self):
        from scan_module.read_layout import validate_layout
        layout = {1: 1, "b": 2}  # key should be string
        is_valid, errors = validate_layout(layout)
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
    
    def test_negative_values(self):
        from scan_module.read_layout import validate_layout
        layout = {"a": 1, "b": -2, "c": 3}
        is_valid, errors = validate_layout(layout)
        self.assertFalse(is_valid)
        # Проверяем, что есть ошибка про отрицательное значение
        negative_errors = [e for e in errors if "отрицательным" in e]
        self.assertGreater(len(negative_errors), 0)
    
    def test_empty_layout(self):
        from scan_module.read_layout import validate_layout
        layout = {}
        is_valid, errors = validate_layout(layout)
        self.assertFalse(is_valid)
        self.assertIn("не может быть пустой", errors[0])

if __name__ == '__main__':
    unittest.main()