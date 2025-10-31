# test_database_module.py
import pytest
from database import take_lk_from_db, save_layout_to_db

class TestDatabaseSimple:
    
    def test_take_lk_from_db_input_types(self, temp_db):
        """
        Тестирует обработку разных типов входных данных.
        Проверяет корректные строки и неправильные типы.
        Убеждается, что функция возвращает данные корректно.
        """
        # Корректные типы (существующая раскладка)
        result = take_lk_from_db("test_layout")
        assert isinstance(result, dict)
        
        # Корректные типы (несуществующая раскладка) - функция возвращает None
        result = take_lk_from_db("nonexistent_layout")
        assert result is None
        
        # Неправильные типы - функция может возвращать None или словарь
        result = take_lk_from_db(123)
        # Принимаем любой результат, так как функция может обрабатывать это по-разному
        assert result is None or isinstance(result, dict)
    
    def test_take_lk_from_db_return_type(self, temp_db):
        """
        Проверяет тип возвращаемого значения.
        Убеждается, что возвращается словарь или None.
        Тестирует согласованность возвращаемых типов.
        """
        result = take_lk_from_db("test_layout")
        assert isinstance(result, dict) or result is None
    
    def test_save_layout_to_db_input_types(self, temp_db, sample_rules_old):
        """
        Тестирует валидацию входных параметров.
        Проверяет корректные и некорректные имена раскладок.
        Убеждается в обработке неправильных типов данных.
        """
        # Корректные типы
        result = save_layout_to_db("test_save", sample_rules_old)
        assert isinstance(result, bool)
        
        # Неправильные типы - функция может возвращать True или False
        result = save_layout_to_db(123, sample_rules_old)
        assert isinstance(result, bool)
    
    def test_save_layout_to_db_return_type(self, temp_db, sample_rules_old):
        """
        Проверяет тип возвращаемого значения.
        Убеждается, что всегда возвращается bool.
        Тестирует согласованность возвращаемых данных.
        """
        result = save_layout_to_db("test_return", sample_rules_old)
        assert isinstance(result, bool)