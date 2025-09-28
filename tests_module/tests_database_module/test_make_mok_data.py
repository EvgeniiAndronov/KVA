import pytest
import sqlite3
from unittest.mock import Mock, patch
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from database_module.db_init import make_mok_data

class TestMakeMokData:
    
    def test_make_mok_data_creates_36_records(self):
        """
        Тест, который проверяет корректное 
        создание тестовых данных в БД
        """
        with patch('database_module.db_init.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            
            make_mok_data('a', 'test_layout')
            
            assert mock_cursor.execute.call_count == 36
            
            mock_cursor.execute.assert_any_call(
                "insert into lk (name_lk, letter, error) VALUES (?, ?, ?)",
                ('test_layout', 'a', 0)
            )
            
            mock_conn.commit.assert_called_once()
            mock_conn.close.assert_called_once()
    
    def test_make_mok_data_exception_handling(self):
        """
        Тест, который проверяет обработку ошибок 
        базы данных
        """
        with patch('database_module.db_init.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            
            mock_cursor.execute.side_effect = sqlite3.Error("Insert error")
            
            with pytest.raises(sqlite3.Error):
                make_mok_data('a', 'test_layout')