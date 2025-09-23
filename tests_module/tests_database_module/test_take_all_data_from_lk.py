import pytest
from unittest.mock import Mock, patch
from database import take_all_data_from_lk


class TestTakeAllDataFromLk:
    """Тесты для функции take_all_data_from_lk"""
    
    def test_take_all_data_success(self):
        """Тест успешного получения всех данных"""
        # Мокируем тестовые данные
        test_data = [
            (1, 'layout1', 'a', 1),
            (2, 'layout1', 'b', 2),
            (3, 'layout2', 'a', 5),
            (4, 'test_layout', 'c', 3)
        ]
        
        with patch('database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchall.return_value = test_data
            
            result = take_all_data_from_lk()
            
            # Проверяем правильность вызовов
            mock_connect.assert_called_once_with("database.db")
            mock_cursor.execute.assert_called_once_with("select * from lk")
            mock_conn.commit.assert_called_once()
            mock_conn.close.assert_called_once()
            
            # Проверяем результат
            assert result == test_data
    
    def test_take_all_data_empty(self):
        """Тест получения данных из пустой таблицы"""
        with patch('database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchall.return_value = []  # Пустая таблица
            
            result = take_all_data_from_lk()
            
            assert result == []
            mock_conn.close.assert_called_once()
    
    def test_database_connection(self):
        """Тест правильности соединения с БД"""
        with patch('database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchall.return_value = []
            
            take_all_data_from_lk()
            
            mock_connect.assert_called_once_with("database.db")