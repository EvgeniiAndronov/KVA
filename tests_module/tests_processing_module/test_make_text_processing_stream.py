import pytest
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'processing_module'))
from calculate_data import make_text_processing_stream

class TestMakeTextProcessingStream:
    """Тесты для функции make_text_processing_stream"""
    
    def test_make_text_processing_stream_basic(self):
        """Тест базовой потоковой обработки текста"""
        def text_generator():
            yield "тест "
            yield "пример"
        
        rules = {'т': 1, 'е': 0, 'с': 2, ' ': 0, 'п': 2, 'р': 1, 'и': 0, 'м': 1}
        
        with patch('calculate_data.tqdm') as mock_tqdm:
            mock_pbar = MagicMock()
            mock_tqdm.return_value = mock_pbar
            
            result = make_text_processing_stream(text_generator(), rules, total_chars=11)
            
            # Правильный расчет: 4 + 0 + 5 = 9 ошибок
            # Всего символов: 5 + 6 = 11
            assert result['total_errors'] == 9
            assert result['total_words'] == 2  # "тест" и "пример"
            assert result['total_characters'] == 11
            assert result['processed_characters'] == 11
            assert result['unknown_characters'] == set()
            assert result['text_type'] == 'continuous'
            assert mock_pbar.update.call_count == 2
            assert mock_pbar.close.called
    
    def test_make_text_processing_stream_with_unknown_chars(self):
        """Тест потоковой обработки с неизвестными символами"""
        def text_generator():
            yield "abc "
            yield "def"
        
        rules = {'a': 1, 'b': 2, 'c': 0}  # d,e,f,пробел - неизвестны
        
        with patch('calculate_data.tqdm') as mock_tqdm:
            mock_pbar = MagicMock()
            mock_tqdm.return_value = mock_pbar
            
            result = make_text_processing_stream(text_generator(), rules)
            
            # Правильный расчет: "abc" = a1+b2+c0 = 3, остальное неизвестно = 0
            # Всего символов: 4 + 3 = 7
            # Обработано: 3 (только a,b,c)
            assert result['total_errors'] == 3
            assert result['total_words'] == 2  # "abc" и "def"
            assert result['total_characters'] == 7  # включая пробел
            assert result['processed_characters'] == 3  # только a,b,c
            assert result['unknown_characters'] == {' ', 'd', 'e', 'f'}
    
    def test_make_text_processing_stream_empty_generator(self):
        """Тест с пустым генератором текста"""
        def empty_generator():
            yield from []
        
        rules = {'a': 1, 'b': 2}
        
        with patch('calculate_data.tqdm') as mock_tqdm:
            mock_pbar = MagicMock()
            mock_tqdm.return_value = mock_pbar
            
            result = make_text_processing_stream(empty_generator(), rules)
            
            assert result['total_errors'] == 0
            assert result['total_words'] == 0
            assert result['total_characters'] == 0
            assert result['processed_characters'] == 0
            assert result['unknown_characters'] == set()
            assert result['avg_errors_per_word'] == 0
            assert result['avg_errors_per_char'] == 0
            assert result['text_type'] == 'continuous'
            assert mock_pbar.close.called