import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'processing_module'))
from calculate_data import validate_rules

class TestValidateRules:
    """Тесты для функции validate_rules"""
    
    def test_validate_rules_correct(self):
        """Тест корректных правил"""
        rules = {'a': 1, 'b': 2, 'c': 0.5}
        
        assert validate_rules(rules) == True
    
    def test_validate_rules_empty_dict(self):
        """Тест пустого словаря правил"""
        with pytest.raises(ValueError, match="Словарь правил не может быть пустым"):
            validate_rules({})
    
    def test_validate_rules_wrong_key_type(self):
        """Тест неправильного типа ключа"""
        rules = {123: 1}  # ключ не строка
        
        with pytest.raises(ValueError, match="Ключ правила должен быть строкой"):
            validate_rules(rules)
    
    def test_validate_rules_wrong_value_type(self):
        """Тест неправильного типа значения"""
        rules = {'a': "1"}  # значение не число
        
        with pytest.raises(ValueError, match="Значение правила должно быть числом"):
            validate_rules(rules)
    
    def test_validate_rules_negative_value(self):
        """Тест отрицательного значения"""
        rules = {'a': -1}
        
        with pytest.raises(ValueError, match="Значение правила не может быть отрицательным"):
            validate_rules(rules)
    
    def test_validate_rules_not_dict(self):
        """Тест что передается не словарь"""
        with pytest.raises(ValueError, match="Правила должны быть словарем"):
            validate_rules("not_a_dict")