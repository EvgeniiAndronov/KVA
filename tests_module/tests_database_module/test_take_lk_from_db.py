import pytest
from unittest.mock import Mock, patch
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from database_module.database import take_lk_from_db


class TestTakeLkFromDb:
    
    def test_take_lk_from_db_success(self):
        """
        Тест, который проверяет успешное 
        получение раскладки из БД
        """
        test_data = [
            ('a', 1), ('b', 2), ('c', 3), ('d', 4), ('e', 5),
            ('f', 6), ('g', 7), ('h', 8), ('i', 9), ('j', 10),
            ('k', 11), ('l', 12), ('m', 13), ('n', 14), ('o', 15)
        ]
        
        with patch('database_module.database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchall.return_value = test_data
            
            result = take_lk_from_db('test_layout')
            
            expected_result = {letter: error for letter, error in test_data}
            assert result == expected_result
    
    def test_take_lk_from_db_insufficient_data(self):
        """
        Тест, который проверяет обработку 
        недостаточного количества данных
        """
        test_data = [('a', 1), ('b', 2)]  # Всего 2 записи
        
        with patch('database_module.database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchall.return_value = test_data
            
            result = take_lk_from_db('small_layout')
            assert result is None
    
    def test_take_lk_from_db_no_data(self):
        """
        Тест, который проверяет поведение 
        при полном отсутствии данных
        """
        with patch('database_module.database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchall.return_value = []
            
            result = take_lk_from_db('nonexistent_layout')
            assert result is None