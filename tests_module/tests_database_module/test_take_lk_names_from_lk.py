import pytest
from unittest.mock import Mock, patch
import sys
import os

# Исправляем импорт
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from database_module.database import take_lk_names_from_lk


class TestTakeLkNamesFromLk:
    
    def test_take_lk_names_returns_data_from_db(self):
        """
        Тест, который проверяет нормальную работу функции,
        когда БД возвращает данные
        """
        test_data = [('layout1',), ('layout2',), ('test_layout',)]
        
        with patch('database_module.database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchall.return_value = test_data
            
            result = take_lk_names_from_lk()
            
            assert result == test_data
            
            mock_cursor.execute.assert_called_once_with("select distinct name_lk from lk")
            mock_conn.close.assert_called_once()
    
    def test_take_lk_names_empty_db(self):
        """
        Тест, который проверяет поведение функции 
        при пустой базе данных
        """
        with patch('database_module.database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchall.return_value = []
            
            result = take_lk_names_from_lk()
            
            assert result == []
    
    def test_take_lk_names_db_error(self):
        """
        Тест, которыйы проверяет обработку 
        ошибок БД
        """
        with patch('database_module.database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.execute.side_effect = Exception("DB error")
            
            with pytest.raises(Exception, match="DB error"):
                take_lk_names_from_lk()