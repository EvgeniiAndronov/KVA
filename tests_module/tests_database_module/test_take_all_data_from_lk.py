import pytest
from unittest.mock import Mock, patch
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from database_module.database import take_all_data_from_lk


class TestTakeAllDataFromLk:
    
    def test_take_all_data_from_lk(self):
        """
        Тест, который проверяет успешное 
        получение всех данных из таблицы lk
        """
        test_data = [
            (1, 'layout1', 'a', 1),
            (2, 'layout1', 'b', 2),
            (3, 'layout2', 'a', 5)
        ]
        
        with patch('database_module.database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchall.return_value = test_data
            
            result = take_all_data_from_lk()
            assert result == test_data
    
    def test_take_all_data_from_lk_empty(self):
        """
        Тест, который проверяет поведение 
        функции при пустой таблице
        """
        with patch('database_module.database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchall.return_value = []
            
            result = take_all_data_from_lk()
            assert result == []