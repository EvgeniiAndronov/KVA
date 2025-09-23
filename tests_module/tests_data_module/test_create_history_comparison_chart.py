import pytest
import os
import tempfile
import sqlite3
from unittest.mock import patch, Mock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'data_module'))
from make_export_plot import create_history_comparison_chart

class TestCreateHistoryComparisonChart:
    """Тесты для функции create_history_comparison_chart"""
    
    @patch('make_export_plot.sqlite3.connect')
    def test_create_history_comparison_chart_success(self, mock_connect):
        """Тест успешного создания графика истории"""
        # Мокаем соединение с БД
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Мокаем данные из БД
        mock_cursor.fetchall.return_value = [
            (1, 10, 'words'), (2, 8, 'words'), (3, 5, 'words'),
            (4, 7, 'words'), (5, 3, 'words')
        ]
        
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = create_history_comparison_chart(
                layout_name="test_layout",
                output_dir=temp_dir
            )
            
            assert file_path is not None
            assert os.path.exists(file_path)
            assert file_path.endswith('.png')
            assert "history_comparison" in file_path
    
    @patch('make_export_plot.sqlite3.connect')
    def test_create_history_comparison_chart_insufficient_data(self, mock_connect):
        """Тест с недостаточным количеством данных"""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Только одна запись - недостаточно для графика
        mock_cursor.fetchall.return_value = [(1, 10, 'words')]
        
        file_path = create_history_comparison_chart(
            layout_name="test_layout"
        )
        
        assert file_path is None
    
    @patch('make_export_plot.sqlite3.connect')
    def test_create_history_comparison_chart_db_error(self, mock_connect):
        """Тест обработки ошибки базы данных"""
        mock_connect.side_effect = sqlite3.Error("DB connection error")
        
        file_path = create_history_comparison_chart(
            layout_name="test_layout"
        )
        
        assert file_path is None