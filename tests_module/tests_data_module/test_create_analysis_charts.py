import pytest
import os
import tempfile
from unittest.mock import patch, Mock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'data_module'))
from make_export_plot import create_analysis_charts

class TestCreateAnalysisCharts:
    """Тесты для функции create_analysis_charts"""
    
    @patch('make_export_plot._create_coverage_pie_chart')
    @patch('make_export_plot._create_error_distribution_chart')
    @patch('make_export_plot._create_metrics_comparison_chart')
    def test_create_analysis_charts_success(self, mock_metrics, mock_error, mock_coverage):
        """Тест успешного создания всех графиков"""
        mock_coverage.return_value = "/path/coverage.png"
        mock_error.return_value = "/path/error.png"
        mock_metrics.return_value = "/path/metrics.png"
        
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
        
        with tempfile.TemporaryDirectory() as temp_dir:
            charts = create_analysis_charts(
                result=sample_result,
                layout_name="test_layout",
                file_path="/test/path.txt",
                output_dir=temp_dir
            )
            
            assert len(charts) == 3
            assert "/path/coverage.png" in charts
            assert mock_coverage.called
            assert mock_error.called
            assert mock_metrics.called
    
    @patch('make_export_plot._create_coverage_pie_chart')
    @patch('make_export_plot._create_error_distribution_chart')
    @patch('make_export_plot._create_metrics_comparison_chart')
    def test_create_analysis_charts_partial_success(self, mock_metrics, mock_error, mock_coverage):
        """Тест когда создаются не все графики"""
        mock_coverage.return_value = "/path/coverage.png"
        mock_error.return_value = None  # ошибка при создании
        mock_metrics.return_value = "/path/metrics.png"
        
        sample_result = {
            'total_errors': 100,
            'total_words': 50,
            'total_characters': 200,
            'processed_characters': 180,
            'unknown_characters': set(),
            'avg_errors_per_word': 2.0,
            'avg_errors_per_char': 0.01,
            'text_type': 'words'
        }
        
        charts = create_analysis_charts(
            result=sample_result,
            layout_name="test_layout",
            file_path="/test/path.txt"
        )
        
        assert len(charts) == 2
        assert None not in charts
    
    @patch('make_export_plot._create_coverage_pie_chart')
    @patch('make_export_plot._create_error_distribution_chart')
    @patch('make_export_plot._create_metrics_comparison_chart')
    def test_create_analysis_charts_minimal_data(self, mock_metrics, mock_error, mock_coverage):
        """Тест с минимальными корректными данными"""
        mock_coverage.return_value = "/path/coverage.png"
        mock_error.return_value = "/path/error.png"
        mock_metrics.return_value = "/path/metrics.png"
        
        # Используем минимальные корректные значения вместо нулей
        sample_result = {
            'total_errors': 1,
            'total_words': 1,
            'total_characters': 10,
            'processed_characters': 8,
            'unknown_characters': set(),
            'avg_errors_per_word': 1.0,
            'avg_errors_per_char': 0.1,
            'text_type': 'words'
        }
        
        charts = create_analysis_charts(
            result=sample_result,
            layout_name="minimal_layout",
            file_path="/test/path.txt"
        )
        
        assert isinstance(charts, list)
        assert mock_coverage.called
        assert mock_error.called
        assert mock_metrics.called