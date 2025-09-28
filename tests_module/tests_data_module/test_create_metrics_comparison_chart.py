import pytest
import os
import tempfile
from unittest.mock import patch, Mock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'data_module'))
from make_export_plot import _create_metrics_comparison_chart

class TestCreateMetricsComparisonChart:
    
    def test_create_metrics_comparison_chart_success(self):
        """
        Тест, который проверяет успешное 
        создание радарной диаграммы
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            sample_result = {
                'total_errors': 100,
                'total_words': 200,
                'total_characters': 1000,
                'processed_characters': 950,
                'unknown_characters': {'@', '#'},
                'avg_errors_per_word': 0.5,
                'avg_errors_per_char': 0.001,
                'text_type': 'words'
            }
            
            file_path = _create_metrics_comparison_chart(
                result=sample_result,
                layout_name="test_layout",
                timestamp="20240101_120000",
                output_dir=temp_dir
            )
            
            assert file_path is not None
            assert os.path.exists(file_path)
            assert file_path.endswith('.png')
            assert "metrics_radar" in file_path
    
    def test_create_metrics_comparison_chart_high_errors(self):
        """
        Тест, который проверяет создание 
        диаграммы с высоким уровнем ошибок
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            sample_result = {
                'total_errors': 1000,
                'total_words': 100,
                'total_characters': 500,
                'processed_characters': 400,
                'unknown_characters': {'@', '#', '$', '%'},
                'avg_errors_per_word': 10.0,
                'avg_errors_per_char': 2.0,
                'text_type': 'words'
            }
            
            file_path = _create_metrics_comparison_chart(
                result=sample_result,
                layout_name="high_error_layout",
                timestamp="20240101_120000",
                output_dir=temp_dir
            )
            
            assert file_path is not None
            assert os.path.exists(file_path)
    
    @patch('make_export_plot.plt.subplot')
    def test_create_metrics_comparison_chart_exception(self, mock_subplot):
        """
        Тест, который проверяет обработку исключения 
        при создании радарной диаграммы
        """
        mock_subplot.side_effect = Exception("Plot error")
        
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
        
        file_path = _create_metrics_comparison_chart(
            result=sample_result,
            layout_name="test_layout",
            timestamp="20240101_120000",
            output_dir="/tmp"
        )
        
        assert file_path is None