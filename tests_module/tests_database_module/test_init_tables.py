import pytest
import sqlite3
from unittest.mock import Mock, patch
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from database_module.db_init import init_tables

class TestInitTables:
    
    def test_init_tables_creates_both_tables(self):
        """
        Тест, который проверяет успешное 
        создание таблиц в базе данных
        """
        with patch('database_module.db_init.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            
            init_tables()
            
            assert mock_cursor.execute.call_count == 2
            mock_conn.commit.assert_called_once()
            mock_conn.close.assert_called_once()
    
    def test_init_tables_exception_handling(self):
        """
        Тест, который проверяет обработку 
        ошибок при создании таблиц
        """
        with patch('database_module.db_init.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            
            mock_cursor.execute.side_effect = sqlite3.Error("Database error")
            
            with pytest.raises(sqlite3.Error):
                init_tables()