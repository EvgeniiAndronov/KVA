import pytest
from database_module.database import take_lk_from_db

class TestTakeLkFromDb:
    
    def test_take_lk_from_db_success(self, mock_db_connection, sample_layout_data):
        """
        Тест, который проверяет успешное 
        получение раскладки из БД
        """
        mock_connect, mock_conn, mock_cursor = mock_db_connection
        mock_cursor.fetchall.return_value = sample_layout_data
        
        result = take_lk_from_db('test_layout')
        
        expected_result = {letter: error for letter, error in sample_layout_data}
        assert result == expected_result
    
    def test_take_lk_from_db_insufficient_data(self, mock_db_connection):
        """
        Тест, который проверяет обработку 
        недостаточного количества данных
        """
        mock_connect, mock_conn, mock_cursor = mock_db_connection
        test_data = [('a', 1), ('b', 2)]  # Всего 2 записи
        mock_cursor.fetchall.return_value = test_data
        
        result = take_lk_from_db('small_layout')
        assert result is None
    
    def test_take_lk_from_db_no_data(self, mock_db_connection):
        """
        Тест, который проверяет поведение 
        при полном отсутствии данных
        """
        mock_connect, mock_conn, mock_cursor = mock_db_connection
        mock_cursor.fetchall.return_value = []
        
        result = take_lk_from_db('nonexistent_layout')
        assert result is None