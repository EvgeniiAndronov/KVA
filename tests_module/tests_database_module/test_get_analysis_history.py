import pytest
from database_module.database import get_analysis_history

class TestGetAnalysisHistory:
    
    def test_get_history_all_layouts(self, mock_db_connection, sample_analysis_history):
        """
        Тест, который проверяет получение 
        истории анализа для всех раскладок
        """
        mock_connect, mock_conn, mock_cursor = mock_db_connection
        mock_cursor.fetchall.return_value = sample_analysis_history
        
        result = get_analysis_history()  # Без указания layout_name
        
        # Проверяем вызов без фильтра по раскладке
        mock_cursor.execute.assert_called_once_with(
            "SELECT id, name_lk, count_errors, type_test FROM data ORDER BY id DESC LIMIT ?",
            (50,)  # limit по умолчанию
        )
        mock_conn.close.assert_called_once()
        
        assert result == sample_analysis_history
    
    def test_get_history_specific_layout(self, mock_db_connection):
        """
        Тест, который проверяет получение 
        истории для конкретной раскладки
        """
        mock_connect, mock_conn, mock_cursor = mock_db_connection
        test_data = [
            (1, 'layout1', 5, 'words|file1.txt|100w|500c'),
            (3, 'layout1', 7, 'words|file3.txt|150w|750c')
        ]
        mock_cursor.fetchall.return_value = test_data
        
        result = get_analysis_history(layout_name='layout1')
        
        # Проверяем вызов с фильтром по раскладке
        mock_cursor.execute.assert_called_once_with(
            "SELECT id, name_lk, count_errors, type_test FROM data WHERE name_lk = ? ORDER BY id DESC LIMIT ?",
            ('layout1', 50)
        )
        
        assert result == test_data
    
    def test_get_history_custom_limit(self, mock_db_connection):
        """
        Тест, который проверяет работу с 
        пользовательским лимитом записей
        """
        mock_connect, mock_conn, mock_cursor = mock_db_connection
        test_data = [
            (1, 'layout1', 5, 'words|file1.txt|100w|500c'),
            (2, 'layout2', 3, 'text|file2.txt|50w|250c')
        ]
        mock_cursor.fetchall.return_value = test_data
        
        result = get_analysis_history(limit=10)
        
        # Проверяем вызов с кастомным лимитом
        mock_cursor.execute.assert_called_once_with(
            "SELECT id, name_lk, count_errors, type_test FROM data ORDER BY id DESC LIMIT ?",
            (10,)
        )
        
        assert result == test_data
    
    def test_get_history_empty(self, mock_db_connection):
        """
        Тест, который проверяет поведение 
        при пустой истории
        """
        mock_connect, mock_conn, mock_cursor = mock_db_connection
        mock_cursor.fetchall.return_value = []  # Пустая история
        
        result = get_analysis_history()
        
        assert result == []
    
    def test_get_history_combined_params(self, mock_db_connection):
        """
        Тест, который проверяет работу 
        с обоими параметрами одновременно
        """
        mock_connect, mock_conn, mock_cursor = mock_db_connection
        test_data = [
            (5, 'specific_layout', 2, 'text|file.txt|10w|50c')
        ]
        mock_cursor.fetchall.return_value = test_data
        
        result = get_analysis_history(layout_name='specific_layout', limit=5)
        
        # Проверяем вызов с обоими параметрами
        mock_cursor.execute.assert_called_once_with(
            "SELECT id, name_lk, count_errors, type_test FROM data WHERE name_lk = ? ORDER BY id DESC LIMIT ?",
            ('specific_layout', 5)
        )
        
        assert result == test_data