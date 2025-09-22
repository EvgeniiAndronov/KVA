import pytest
from unittest.mock import Mock, patch
from database import save_analysis_result


class TestSaveAnalysisResult:
    """Тесты для функции save_analysis_result"""
    
    def test_save_analysis_result_words_type(self):
        """Тест сохранения результата анализа слов"""
        test_result = {
            'total_errors': 5,
            'total_words': 100,
            'total_characters': 500
        }
        
        with patch('database.sqlite3.connect') as mock_connect:
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
            mock_connect.assert_called_once_with("database.db")
            mock_cursor.execute.assert_called_once_with(
                "INSERT INTO data (name_lk, count_errors, type_test) VALUES (?, ?, ?)",
                ('test_layout', 5, 'words|/path/to/file.txt|100w|500c')
            )
            mock_conn.commit.assert_called_once()
            mock_conn.close.assert_called_once()
            
            # Проверяем возвращаемый ID
            assert record_id == 42
    
    def test_save_analysis_result_text_type(self):
        """Тест сохранения результата анализа текста"""
        test_result = {
            'total_errors': 3,
            'total_words': 50,
            'total_characters': 250
        }
        
        with patch('database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.lastrowid = 43
            
            record_id = save_analysis_result(
                layout_name='another_layout',
                result=test_result,
                file_path='/path/to/text.txt',
                analysis_type='text'
            )
            
            expected_test_type = 'text|/path/to/text.txt|50w|250c'
            mock_cursor.execute.assert_called_once_with(
                "INSERT INTO data (name_lk, count_errors, type_test) VALUES (?, ?, ?)",
                ('another_layout', 3, expected_test_type)
            )
            assert record_id == 43
    
    def test_save_analysis_result_default_type(self):
        """Тест сохранения с типом анализа по умолчанию"""
        test_result = {
            'total_errors': 10,
            'total_words': 200,
            'total_characters': 1000
        }
        
        with patch('database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.lastrowid = 44
            
            record_id = save_analysis_result(
                layout_name='default_layout',
                result=test_result,
                file_path='/path/to/default.txt'
                # analysis_type не указан, должен быть 'words' по умолчанию
            )
            
            expected_test_type = 'words|/path/to/default.txt|200w|1000c'
            mock_cursor.execute.assert_called_once_with(
                "INSERT INTO data (name_lk, count_errors, type_test) VALUES (?, ?, ?)",
                ('default_layout', 10, expected_test_type)
            )
            assert record_id == 44
    
    def test_save_analysis_result_special_characters(self):
        """Тест с специальными символами в путях и именах"""
        test_result = {
            'total_errors': 1,
            'total_words': 10,
            'total_characters': 50
        }
        
        with patch('database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.lastrowid = 45
            
            record_id = save_analysis_result(
                layout_name='layout with spaces',
                result=test_result,
                file_path='C:/Program Files/test/file.txt',
                analysis_type='text'
            )
            
            expected_test_type = 'text|C:/Program Files/test/file.txt|10w|50c'
            mock_cursor.execute.assert_called_once_with(
                "INSERT INTO data (name_lk, count_errors, type_test) VALUES (?, ?, ?)",
                ('layout with spaces', 1, expected_test_type)
            )
            assert record_id == 45