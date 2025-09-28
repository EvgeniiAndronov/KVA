import pytest
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'processing_module'))
from calculate_data import make_processing_stream

class TestMakeProcessingStream:
    
    def test_make_processing_stream_basic(self):
        """
        Тест, который проверяет базовую функциональность 
        потоковой обработки
        """
        def word_generator():
            yield ["тест", "слово"]
            yield ["пример"]
        
        rules = {'т': 1, 'е': 0, 'с': 2, 'л': 1, 'о': 0, 'в': 1, 'п': 2, 'р': 1, 'и': 0, 'м': 1}
        
        with patch('calculate_data.tqdm') as mock_tqdm:
            mock_pbar = MagicMock()
            mock_tqdm.return_value = mock_pbar
            
            result = make_processing_stream(word_generator(), rules, total_words=3)
            
            # Правильный расчет: 4 + 4 + 5 = 13 ошибок
            # Всего символов: 4 + 5 + 6 = 15
            assert result['total_errors'] == 13
            assert result['total_words'] == 3
            assert result['total_characters'] == 15
            assert result['processed_characters'] == 15
            assert result['unknown_characters'] == set()
            assert mock_pbar.update.call_count == 2
            assert mock_pbar.close.called
    
    def test_make_processing_stream_with_unknown_chars(self):
        """
        Тест, который проверяет потоковую обработку 
        с неизвестными символами
        """
        def word_generator():
            yield ["abc", "def"]
            yield ["ghi"]
        
        rules = {'a': 1, 'b': 2, 'c': 0}  # d,e,f,g,h,i - неизвестны
        
        with patch('calculate_data.tqdm') as mock_tqdm:
            mock_pbar = MagicMock()
            mock_tqdm.return_value = mock_pbar
            
            result = make_processing_stream(word_generator(), rules)
            
            # Правильный расчет: "abc" = a1+b2+c0 = 3, остальные слова неизвестны = 0
            # Всего символов: 3 + 3 + 3 = 9
            # Обработано: 3 (только "abc")
            assert result['total_errors'] == 3
            assert result['total_words'] == 3
            assert result['total_characters'] == 9
            assert result['processed_characters'] == 3
            assert result['unknown_characters'] == {'d', 'e', 'f', 'g', 'h', 'i'}
    
    def test_make_processing_stream_empty_generator(self):
        """
        Тест, который проверяет обработку пустого генератора
        """
        def empty_generator():
            yield from []
        
        rules = {'a': 1, 'b': 2}
        
        with patch('calculate_data.tqdm') as mock_tqdm:
            mock_pbar = MagicMock()
            mock_tqdm.return_value = mock_pbar
            
            result = make_processing_stream(empty_generator(), rules)
            
            assert result['total_errors'] == 0
            assert result['total_words'] == 0
            assert result['total_characters'] == 0
            assert result['processed_characters'] == 0
            assert result['unknown_characters'] == set()
            assert result['avg_errors_per_word'] == 0
            assert result['avg_errors_per_char'] == 0
            assert mock_pbar.close.called