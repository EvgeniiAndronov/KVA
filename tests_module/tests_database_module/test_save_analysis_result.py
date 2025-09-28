import pytest
from unittest.mock import Mock, patch
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from database_module.database import save_analysis_result


class TestSaveAnalysisResult:
    
    def test_save_analysis_result_words_type(self):
        """
        Тест, который проверяет сохранение 
        результатов анализа для типа 
        'words' (слова)
        """
        test_result = {
            'total_errors': 5,
            'total_words': 100,
            'total_characters': 500
        }
        
        with patch('database_module.database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.lastrowid = 42  # Мок ID созданной записи
            
            record_id = save_analysis_result(
                layout_name='test_layout',
                result=test_result,
                file_path='/path/to/file.txt',
                analysis_type='words'
            )
            
            # Проверяем правильность вызовов
            mock_cursor.execute.assert_called_once_with(
                "INSERT INTO data (name_lk, count_errors, type_test) VALUES (?, ?, ?)",
                ('test_layout', 5, 'words|/path/to/file.txt|100w|500c')
            )
            mock_conn.commit.assert_called_once()
            mock_conn.close.assert_called_once()
            
            # Проверяем возвращаемый ID
            assert record_id == 42