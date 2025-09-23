import pytest
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'processing_module'))
from calculate_data import make_processing

class TestMakeProcessing:
    """Тесты для функции make_processing"""
    
    def test_make_processing_basic(self):
        """Тест базовой функциональности"""
        wordlist = ["тест", "слово", "пример"]
        rules = {'т': 1, 'е': 0, 'с': 2, 'л': 1, 'о': 0, 'в': 1, 'п': 2, 'р': 1, 'и': 0, 'м': 1}
        
        result = make_processing(wordlist, rules)
        
        # Правильный расчет: 
        # "тест" = т1+е0+с2+т1 = 4
        # "слово" = с2+л1+о0+в1+о0 = 4  
        # "пример" = п2+р1+и0+м1+е0+р1 = 5
        # Итого ошибок: 4 + 4 + 5 = 13
        # Всего символов: 4 + 5 + 6 = 15
        assert result['total_errors'] == 13
        assert result['total_words'] == 3
        assert result['total_characters'] == 15  # 4 + 5 + 6 = 15
        assert result['processed_characters'] == 15
        assert result['unknown_characters'] == set()
        assert result['avg_errors_per_word'] == pytest.approx(13/3, 0.01)
        assert result['avg_errors_per_char'] == pytest.approx(13/15, 0.01)
    
    def test_make_processing_with_unknown_chars(self):
        """Тест с неизвестными символами"""
        wordlist = ["test", "word"]
        rules = {'t': 1, 'e': 0, 's': 2}  # отсутствуют w, o, r, d
        
        result = make_processing(wordlist, rules)
        
        # Правильный расчет:
        # "test" = t1+e0+s2+t1 = 4 (все символы известны)
        # "word" = w?+o?+r?+d? = 0 (все символы неизвестны)
        # Итого ошибок: 4 + 0 = 4
        # Всего символов: 4 + 4 = 8
        # Обработано: 4 (только "test")
        assert result['total_errors'] == 4
        assert result['total_words'] == 2
        assert result['total_characters'] == 8
        assert result['processed_characters'] == 4  # только "test" обработан
        assert result['unknown_characters'] == {'w', 'o', 'r', 'd'}
        assert result['avg_errors_per_word'] == 2.0
        assert result['avg_errors_per_char'] == 1.0
    
    def test_make_processing_empty_wordlist(self):
        """Тест с пустым списком слов"""
        wordlist = []
        rules = {'a': 1, 'b': 2}
        
        result = make_processing(wordlist, rules)
        
        assert result['total_errors'] == 0
        assert result['total_words'] == 0
        assert result['total_characters'] == 0
        assert result['processed_characters'] == 0
        assert result['unknown_characters'] == set()
        assert result['avg_errors_per_word'] == 0
        assert result['avg_errors_per_char'] == 0
    
    def test_make_processing_large_list_raises_error(self):
        """Тест что большие списки вызывают ошибку"""
        wordlist = ["word"] * 10001  # 10001 слов
        rules = {'w': 1, 'o': 1, 'r': 1, 'd': 1}
        
        with pytest.raises(ValueError, match="Список слишком большой"):
            make_processing(wordlist, rules)