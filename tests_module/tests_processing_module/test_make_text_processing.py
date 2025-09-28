import pytest
import sys
import os
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'processing_module'))
from calculate_data import make_text_processing

class TestMakeTextProcessing:
    
    def test_make_text_processing_basic(self):
        """
        Тест, который проверяет базовую обработку 
        текста
        """
        text = "тест пример"
        rules = {'т': 1, 'е': 0, 'с': 2, ' ': 0, 'п': 2, 'р': 1, 'и': 0, 'м': 1}
        
        result = make_text_processing(text, rules)
        
        # Правильный расчет: 
        # "тест" = т1+е0+с2+т1 = 4
        # пробел = 0
        # "пример" = п2+р1+и0+м1+е0+р1 = 5
        # Итого ошибок: 4 + 0 + 5 = 9
        # Всего символов: 4 + 1 + 6 = 11
        assert result['total_errors'] == 9
        assert result['total_words'] == 2
        assert result['total_characters'] == 11  # включая пробел
        assert result['processed_characters'] == 11
        assert result['unknown_characters'] == set()
        assert result['text_type'] == 'continuous'
        assert result['avg_errors_per_word'] == 4.5
        assert result['avg_errors_per_char'] == pytest.approx(9/11, 0.01)
    
    def test_make_text_processing_with_unknown_chars(self):
        """
        Тест, который проверяет обработку текста с 
        неизвестными символами
        """
        text = "hello world"
        rules = {'h': 1, 'e': 0, 'l': 2, 'o': 1}  # w, r, d, пробел - неизвестны
        
        result = make_text_processing(text, rules)
        
        # Правильный расчет:
        # "hello" = h1+e0+l2+l2+o1 = 6
        # пробел = ? = 0
        # "world" = w?+o1+r?+l2+d? = 3
        # Итого ошибок: 6 + 0 + 3 = 9
        # Всего символов: 5 + 1 + 5 = 11
        # Обработано: h,e,l,l,o,o,l = 7 символов
        assert result['total_errors'] == 9
        assert result['total_words'] == 2
        assert result['total_characters'] == 11  # включая пробел
        assert result['processed_characters'] == 7  # h,e,l,l,o,o,l
        assert result['unknown_characters'] == {' ', 'w', 'r', 'd'}
    
    def test_make_text_processing_empty_text(self):
        """
        Тест, который проверяет обработку пустого 
        текста
        """
        text = ""
        rules = {'a': 1, 'b': 2}
        
        result = make_text_processing(text, rules)
        
        assert result['total_errors'] == 0
        assert result['total_words'] == 0
        assert result['total_characters'] == 0
        assert result['processed_characters'] == 0
        assert result['unknown_characters'] == set()
        assert result['avg_errors_per_word'] == 0
        assert result['avg_errors_per_char'] == 0
        assert result['text_type'] == 'continuous'
    
    def test_make_text_processing_large_text_raises_error(self):
        """
        Тест, который проверяет обработку слишком 
        больших текстов
        """
        text = "x" * 100001  # 100001 символов
        rules = {'x': 1}
        
        with pytest.raises(ValueError, match="Текст слишком большой"):
            make_text_processing(text, rules)