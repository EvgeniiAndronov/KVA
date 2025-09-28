import pytest
from unittest.mock import Mock, patch
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from database_module.database import delete_analysis_result


class TestDeleteAnalysisResult:
    
    def test_delete_existing_record(self):
        """
        Тест, который проверяет удаление 
        существующей записи
        """
        with patch('database_module.database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.rowcount = 1  # Запись была удалена
            
            result = delete_analysis_result(record_id=42)
            
            # Проверяем правильность вызовов
            mock_cursor.execute.assert_called_once_with(
                "DELETE FROM data WHERE id = ?", 
                (42,)
            )
            mock_conn.commit.assert_called_once()
            mock_conn.close.assert_called_once()
            
            # Проверяем результат
            assert result is True
    
    def test_delete_nonexistent_record(self):
        """
        Тест, который проверяет попытку 
        удаления несуществующей записи
        """
        with patch('database_module.database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.rowcount = 0  # Запись не найдена
            
            result = delete_analysis_result(record_id=999)
            
            # Проверяем, что запрос выполнен
            mock_cursor.execute.assert_called_once_with(
                "DELETE FROM data WHERE id = ?", 
                (999,)
            )
            mock_conn.commit.assert_called_once()
            
            # Проверяем результат
            assert result is False
    
    def test_delete_multiple_records(self):
        """
        Тест, который проверяет случай, 
        когда удаляется несколько записей
        """
        with patch('database_module.database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.rowcount = 2  # Удалено 2 записи (неожиданно)
            
            result = delete_analysis_result(record_id=42)
            
            # Должен вернуть True, так как записи были удалены
            assert result is True
    
    def test_delete_record_zero_id(self):
        """
        Тест, который проверяет удаление 
        записи с ID=0
        """
        with patch('database_module.database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.rowcount = 0  # ID=0 не существует
            
            result = delete_analysis_result(record_id=0)
            
            mock_cursor.execute.assert_called_once_with(
                "DELETE FROM data WHERE id = ?", 
                (0,)
            )
            assert result is False
    
    @pytest.mark.parametrize("record_id,rowcount,expected", [
        (1, 1, True),    # Существующая запись
        (2, 0, False),   # Несуществующая запись
        (100, 1, True),  # Другая существующая запись
        (-1, 0, False),  # Отрицательный ID
    ])
    def test_various_delete_scenarios(self, record_id, rowcount, expected):
        """
        Параметризованный тест для различных сценариев удаления 
        """
        with patch('database_module.database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.rowcount = rowcount
            
            result = delete_analysis_result(record_id=record_id)
            
            assert result == expected