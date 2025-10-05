import pytest
from unittest.mock import Mock, patch
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from database_module.database import take_all_data_from_lk

class TestTakeAllDataFromLk:
    
    def test_take_all_data_from_lk(self, mock_db_connection, sample_layout_data):
        """
        Тест, который проверяет успешное 
        получение всех данных из таблицы lk
        """
        mock_connect, mock_conn, mock_cursor = mock_db_connection
        mock_cursor.fetchall.return_value = sample_layout_data
        
        result = take_all_data_from_lk()
        assert result == sample_layout_data
    
    def test_take_all_data_from_lk_empty(self, mock_db_connection):
        """
        Тест, который проверяет поведение 
        функции при пустой таблице
        """
        mock_connect, mock_conn, mock_cursor = mock_db_connection
        mock_cursor.fetchall.return_value = []
        
        result = take_all_data_from_lk()
        assert result == []