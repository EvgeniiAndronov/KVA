import pytest
from unittest.mock import Mock, patch
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from database_module.database import get_analysis_statistics


class TestGetAnalysisStatistics:
    
    def test_get_statistics_with_data(self):
        """
        Тест, который проверяет получение 
        статистики при наличии данных
        """
        test_result = (5, 3.5, 1, 7)  # total_tests, avg_errors, min_errors, max_errors
        
        with patch('database_module.database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchone.return_value = test_result
            
            result = get_analysis_statistics('test_layout')
            
            # Проверяем, что execute был вызван
            mock_cursor.execute.assert_called_once()
            
            # Получаем аргументы вызова
            call_args = mock_cursor.execute.call_args
            sql_query = call_args[0][0]
            params = call_args[0][1] if len(call_args[0]) > 1 else ()
            
            # Проверяем ключевые части SQL-запроса
            assert "SELECT" in sql_query
            assert "COUNT(*)" in sql_query
            assert "AVG(count_errors)" in sql_query
            assert "MIN(count_errors)" in sql_query
            assert "MAX(count_errors)" in sql_query
            assert "FROM data" in sql_query
            assert "WHERE name_lk = ?" in sql_query
            assert params == ('test_layout',)
            
            mock_conn.close.assert_called_once()
            
            # Проверяем результат
            expected_result = {
                'total_tests': 5,
                'avg_errors': 3.5,
                'min_errors': 1,
                'max_errors': 7
            }
            assert result == expected_result
    
    def test_get_statistics_no_data(self):
        """
        Тест, который проверяет поведение при 
        отсутствии данных для раскладки
        """
        with patch('database_module.database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchone.return_value = None  # Нет данных
            
            result = get_analysis_statistics('nonexistent_layout')
            
            # Проверяем результат по умолчанию
            expected_result = {
                'total_tests': 0,
                'avg_errors': 0,
                'min_errors': 0,
                'max_errors': 0
            }
            assert result == expected_result
    
    def test_get_statistics_empty_result(self):
        """
        Тест, который проверяет обработку 
        пустого результата
        """
        with patch('database_module.database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchone.return_value = (0, None, None, None)  # COUNT=0
            
            result = get_analysis_statistics('empty_layout')
            
            # Должен вернуть значения по умолчанию
            expected_result = {
                'total_tests': 0,
                'avg_errors': 0,
                'min_errors': 0,
                'max_errors': 0
            }
            assert result == expected_result
    
    def test_get_statistics_special_layout_name(self):
        """
        Тест, который проверяет работу с именами 
        раскладок, содержащими пробелы
        """
        test_result = (2, 4.0, 3, 5)
        
        with patch('database_module.database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchone.return_value = test_result
            
            result = get_analysis_statistics('layout with spaces')
            
            mock_cursor.execute.assert_called_once()
            # Проверяем, что имя раскладки правильно передано в запрос
            call_args = mock_cursor.execute.call_args
            params = call_args[0][1] if len(call_args[0]) > 1 else ()
            assert params == ('layout with spaces',)
            
            expected_result = {
                'total_tests': 2,
                'avg_errors': 4.0,
                'min_errors': 3,
                'max_errors': 5
            }
            assert result == expected_result
    
    def test_get_statistics_null_values(self):
        """
        Тест, который проверяет обработку 
        NULL-значений из БД
        """
        test_result = (3, None, None, None)
    
        with patch('database_module.database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchone.return_value = test_result
        
            result = get_analysis_statistics('layout_with_nulls')
        
            # Если функция не обрабатывает NULL, ожидаем None
            expected_result = {
                'total_tests': 3,
                'avg_errors': None,
                'min_errors': None,
                'max_errors': None
            }
            assert result == expected_result