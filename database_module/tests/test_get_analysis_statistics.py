import pytest
from unittest.mock import Mock, patch
from database import get_analysis_statistics


class TestGetAnalysisStatistics:
    """Тесты для функции get_analysis_statistics"""
    
    def test_get_statistics_with_data(self):
        """Тест получения статистики при наличии данных"""
        test_result = (5, 3.5, 1, 7)  # total_tests, avg_errors, min_errors, max_errors
        
        with patch('database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchone.return_value = test_result
            
            result = get_analysis_statistics('test_layout')
            
            # Проверяем правильность SQL-запроса
            mock_cursor.execute.assert_called_once_with("""
                SELECT 
                    COUNT(*) as total_tests,
                    AVG(count_errors) as avg_errors,
                    MIN(count_errors) as min_errors,
                    MAX(count_errors) as max_errors
                FROM data 
                WHERE name_lk = ?
            """, ('test_layout',))
            
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
        """Тест получения статистики при отсутствии данных"""
        with patch('database.sqlite3.connect') as mock_connect:
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
        """Тест получения статистики при пустом результате"""
        with patch('database.sqlite3.connect') as mock_connect:
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
        """Тест со специальными символами в имени раскладки"""
        test_result = (2, 4.0, 3, 5)
        
        with patch('database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchone.return_value = test_result
            
            result = get_analysis_statistics('layout with spaces')
            
            mock_cursor.execute.assert_called_once()
            # Проверяем, что имя раскладки правильно передано в запрос
            call_args = mock_cursor.execute.call_args
            assert call_args[0][1] == ('layout with spaces',)
            
            expected_result = {
                'total_tests': 2,
                'avg_errors': 4.0,
                'min_errors': 3,
                'max_errors': 5
            }
            assert result == expected_result