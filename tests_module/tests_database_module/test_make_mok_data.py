import pytest
import sqlite3
from database_module.db_init import make_mok_data

class TestMakeMokData:
    
    def test_make_mok_data_creates_36_records(self, mock_db_connection):
        """
        Тест, который проверяет корректное 
        создание тестовых данных в БД
        """
        mock_connect, mock_conn, mock_cursor = mock_db_connection
        
        make_mok_data('a', 'test_layout')
        
        assert mock_cursor.execute.call_count == 36
        
        mock_cursor.execute.assert_any_call(
            "insert into lk (name_lk, letter, error) VALUES (?, ?, ?)",
            ('test_layout', 'a', 0)
        )
        
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
    
    def test_make_mok_data_exception_handling(self, mock_db_connection):
        """
        Тест, который проверяет обработку ошибок 
        базы данных
        """
        mock_connect, mock_conn, mock_cursor = mock_db_connection
        
        mock_cursor.execute.side_effect = sqlite3.Error("Insert error")
        
        with pytest.raises(sqlite3.Error):
            make_mok_data('a', 'test_layout')