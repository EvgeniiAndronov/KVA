import os
import unittest
import json

class TestReadJsonLayout(unittest.TestCase):
    
    def setUp(self):
        """
        Создает имя тестового JSON файла 
        перед каждым тестом
        """
        self.test_file = "test_json.json"
    
    def tearDown(self):
        """
        Удаляет тестовый файл после каждого 
        теста
        """
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_direct_layout(self):
        """
        Тест, который проверяет чтение 
        JSON с прямой структурой {символ: 
        значение}
        """
        from scan_module.read_layout import _read_json_layout
        layout_data = {"a": 1, "b": 2, "c": 3}
        with open(self.test_file, "w", encoding="utf-8") as f:
            json.dump(layout_data, f)
        
        result = _read_json_layout(self.test_file)
        self.assertEqual(result, layout_data)
    
    def test_nested_layout(self):
        """
        Тест, который проверяет чтение JSON с 
        вложенной структурой {layout: {символ: 
        значение}}
        """
        from scan_module.read_layout import _read_json_layout
        layout_data = {"layout": {"a": 1, "b": 2}}
        with open(self.test_file, "w", encoding="utf-8") as f:
            json.dump(layout_data, f)
        
        result = _read_json_layout(self.test_file)
        self.assertEqual(result, {"a": 1, "b": 2})
    
    def test_invalid_json_format(self):
        """
        Тест, который проверяет обработку 
        некорректного JSON формата
        """
        from scan_module.read_layout import _read_json_layout
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("invalid json content")
        
        with self.assertRaises(ValueError):
            _read_json_layout(self.test_file)

if __name__ == '__main__':
    unittest.main()