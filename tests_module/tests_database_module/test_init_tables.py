import pytest
import sqlite3
from database_module.db_init import init_tables

class TestInitTables:
    
    def test_init_tables_creates_both_tables(self, mock_db_connection):
        """
        Тест, который проверяет успешное 
        создание таблиц в базе данных
        """
        mock_connect, mock_conn, mock_cursor = mock_db_connection
        
        init_tables()
        
        assert mock_cursor.execute.call_count == 2
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
    
    def test_init_tables_exception_handling(self, mock_db_connection):
        """
        Тест, который проверяет обработку 
        ошибок при создании таблиц
        """
        mock_connect, mock_conn, mock_cursor = mock_db_connection
        
        mock_cursor.execute.side_effect = sqlite3.Error("Database error")
        
        with pytest.raises(sqlite3.Error):
            init_tables()