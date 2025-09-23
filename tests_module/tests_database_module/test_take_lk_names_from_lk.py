import pytest
from unittest.mock import Mock, patch
import sys
import os

# Исправляем импорт
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from database_module.database import take_lk_names_from_lk


class TestTakeLkNamesFromLk:
    """Тесты для функции take_lk_names_from_lk"""
    
    def test_take_lk_names_returns_data_from_db(self):
        """Тест что функция возвращает данные из базы"""
        test_data = [('layout1',), ('layout2',), ('test_layout',)]
        
        # Исправляем путь в моке
        with patch('database_module.database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchall.return_value = test_data
            
            result = take_lk_names_from_lk()
            
            # Проверяем что функция возвращает то, что получила из БД
            assert result == test_data
            
            # Проверяем что был выполнен правильный SQL-запрос
            mock_cursor.execute.assert_called_once_with("select distinct name_lk from lk")
            mock_conn.close.assert_called_once()
    
    def test_take_lk_names_empty_db(self):
        """Тест пустой базы данных"""
        with patch('database_module.database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchall.return_value = []
            
            result = take_lk_names_from_lk()
            
            assert result == []
    
    def test_take_lk_names_db_error(self):
        """Тест обработки ошибки базы данных"""
        with patch('database_module.database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.execute.side_effect = Exception("DB error")
            
            # Функция не обрабатывает исключения, поэтому тест должен ожидать исключение
            with pytest.raises(Exception, match="DB error"):
                take_lk_names_from_lk()