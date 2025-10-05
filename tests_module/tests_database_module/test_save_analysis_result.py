import pytest
from database_module.database import save_analysis_result

class TestSaveAnalysisResult:
    
    def test_save_analysis_result_words_type(self, mock_db_connection, sample_analysis_result):
        """
        Тест, который проверяет сохранение 
        результатов анализа для типа 
        'words' (слова)
        """
        mock_connect, mock_conn, mock_cursor = mock_db_connection
        mock_cursor.lastrowid = 42  # Мок ID созданной записи
        
        record_id = save_analysis_result(
            layout_name='test_layout',
            result=sample_analysis_result,
            file_path='/path/to/file.txt',
            analysis_type='words'
        )
        
        # Проверяем правильность вызовов
        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO data (name_lk, count_errors, type_test) VALUES (?, ?, ?)",
            ('test_layout', 5, 'words|/path/to/file.txt|100w|500c')
        )
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()
        
        # Проверяем возвращаемый ID
        assert record_id == 42