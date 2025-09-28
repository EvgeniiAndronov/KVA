import pytest
import os
import tempfile
from unittest.mock import patch, Mock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'data_module'))
from make_export_plot import _create_error_distribution_chart

class TestCreateErrorDistributionChart:
    
    def test_create_error_distribution_chart_success(self):
        """
        Тест, который проверяет успешное создание 
        гистограммы распределения ошибок
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            sample_result = {
                'total_errors': 1500,
                'total_words': 1000,
                'total_characters': 5000,
                'processed_characters': 4800,
                'unknown_characters': {'@', '#', '$'},
                'avg_errors_per_word': 1.5,
                'avg_errors_per_char': 0.0003,
                'text_type': 'words'
            }
            
            file_path = _create_error_distribution_chart(
                result=sample_result,
                layout_name="test_layout",
                timestamp="20240101_120000",
                output_dir=temp_dir
            )
            
            assert file_path is not None
            assert os.path.exists(file_path)
            assert file_path.endswith('.png')
            assert "error_distribution" in file_path
    
    def test_create_error_distribution_chart_small_values(self):
        """
        Тест, который проверяет создание гистограммы 
        с малыми значениями ошибок
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            sample_result = {
                'total_errors': 5,
                'total_words': 10,
                'total_characters': 50,
                'processed_characters': 45,
                'unknown_characters': set(),
                'avg_errors_per_word': 0.5,
                'avg_errors_per_char': 0.1,
                'text_type': 'words'
            }
            
            file_path = _create_error_distribution_chart(
                result=sample_result,
                layout_name="small_layout",
                timestamp="20240101_120000",
                output_dir=temp_dir
            )
            
            assert file_path is not None
            assert os.path.exists(file_path)
    
    @patch('make_export_plot.plt.subplots')
    def test_create_error_distribution_chart_exception(self, mock_subplots):
        """
        Тест, который проверяет обработку исключения 
        при создании гистограммы
        """
        mock_subplots.side_effect = Exception("Subplots error")
        
        sample_result = {
            'total_errors': 100,
            'total_words': 50,
            'total_characters': 200,
            'processed_characters': 180,
            'unknown_characters': {'@'},
            'avg_errors_per_word': 2.0,
            'avg_errors_per_char': 0.01,
            'text_type': 'words'
        }
        
        file_path = _create_error_distribution_chart(
            result=sample_result,
            layout_name="test_layout",
            timestamp="20240101_120000",
            output_dir="/tmp"
        )
        
        assert file_path is None