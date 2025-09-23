import pytest
import sqlite3
from unittest.mock import Mock, patch
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from database_module.db_init import make_mok_data

class TestMakeMokData:
    """Тесты для функции make_mok_data"""
    
    def test_make_mok_data_creates_36_records(self):
        """Тест создания 36 записей (русский + английский алфавит)"""
        with patch('database_module.db_init.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            
            make_mok_data('a', 'test_layout')
            
            # Функция создает 36 записей (русский + английский алфавит)
            assert mock_cursor.execute.call_count == 36
            
            # Проверяем первый вызов
            mock_cursor.execute.assert_any_call(
                "insert into lk (name_lk, letter, error) VALUES (?, ?, ?)",
                ('test_layout', 'a', 0)
            )
            
            mock_conn.commit.assert_called_once()
            mock_conn.close.assert_called_once()
    
    def test_make_mok_data_exception_handling(self):
        """Тест обработки исключений"""
        with patch('database_module.db_init.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            
            # Симулируем ошибку при вставке
            mock_cursor.execute.side_effect = sqlite3.Error("Insert error")
            
            # Если функция не обрабатывает исключения, тест должен проверить это поведение
            with pytest.raises(sqlite3.Error):
                make_mok_data('a', 'test_layout')