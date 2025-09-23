import pytest
from unittest.mock import Mock, patch
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from database_module.database import get_analysis_history


class TestGetAnalysisHistory:
    """Тесты для функции get_analysis_history"""
    
    def test_get_history_all_layouts(self):
        """Тест получения истории для всех раскладок"""
        test_data = [
            (1, 'layout1', 5, 'words|file1.txt|100w|500c'),
            (2, 'layout2', 3, 'text|file2.txt|50w|250c'),
            (3, 'layout1', 7, 'words|file3.txt|150w|750c')
        ]
        
        with patch('database_module.database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchall.return_value = test_data
            
            result = get_analysis_history()  # Без указания layout_name
            
            # Проверяем вызов без фильтра по раскладке
            mock_cursor.execute.assert_called_once_with(
                "SELECT id, name_lk, count_errors, type_test FROM data ORDER BY id DESC LIMIT ?",
                (50,)  # limit по умолчанию
            )
            mock_conn.close.assert_called_once()
            
            assert result == test_data
    
    def test_get_history_specific_layout(self):
        """Тест получения истории для конкретной раскладки"""
        test_data = [
            (1, 'layout1', 5, 'words|file1.txt|100w|500c'),
            (3, 'layout1', 7, 'words|file3.txt|150w|750c')
        ]
        
        with patch('database_module.database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchall.return_value = test_data
            
            result = get_analysis_history(layout_name='layout1')
            
            # Проверяем вызов с фильтром по раскладке
            mock_cursor.execute.assert_called_once_with(
                "SELECT id, name_lk, count_errors, type_test FROM data WHERE name_lk = ? ORDER BY id DESC LIMIT ?",
                ('layout1', 50)
            )
            
            assert result == test_data
    
    def test_get_history_custom_limit(self):
        """Тест получения истории с кастомным лимитом"""
        test_data = [
            (1, 'layout1', 5, 'words|file1.txt|100w|500c'),
            (2, 'layout2', 3, 'text|file2.txt|50w|250c')
        ]
        
        with patch('database_module.database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchall.return_value = test_data
            
            result = get_analysis_history(limit=10)
            
            # Проверяем вызов с кастомным лимитом
            mock_cursor.execute.assert_called_once_with(
                "SELECT id, name_lk, count_errors, type_test FROM data ORDER BY id DESC LIMIT ?",
                (10,)
            )
            
            assert result == test_data
    
    def test_get_history_empty(self):
        """Тест получения пустой истории"""
        with patch('database_module.database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchall.return_value = []  # Пустая история
            
            result = get_analysis_history()
            
            assert result == []
    
    def test_get_history_combined_params(self):
        """Тест с комбинацией параметров"""
        test_data = [
            (5, 'specific_layout', 2, 'text|file.txt|10w|50c')
        ]
        
        with patch('database_module.database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchall.return_value = test_data
            
            result = get_analysis_history(layout_name='specific_layout', limit=5)
            
            # Проверяем вызов с обоими параметрами
            mock_cursor.execute.assert_called_once_with(
                "SELECT id, name_lk, count_errors, type_test FROM data WHERE name_lk = ? ORDER BY id DESC LIMIT ?",
                ('specific_layout', 5)
            )
            
            assert result == test_data