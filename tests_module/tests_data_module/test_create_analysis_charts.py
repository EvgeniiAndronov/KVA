import pytest
import os
import tempfile
from unittest.mock import patch, Mock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'data_module'))
from make_export_plot import create_analysis_charts

class TestCreateAnalysisCharts:
    
    @patch('make_export_plot._create_coverage_pie_chart')
    @patch('make_export_plot._create_error_distribution_chart')
    @patch('make_export_plot._create_metrics_comparison_chart')
    def test_create_analysis_charts_success(self, mock_metrics, mock_error, mock_coverage, temp_dir, sample_result_basic):
        """
        Тест, который проверяет успешное создание 
        всех графиков анализа
        """
        mock_coverage.return_value = "/path/coverage.png"
        mock_error.return_value = "/path/error.png"
        mock_metrics.return_value = "/path/metrics.png"
        
        charts = create_analysis_charts(
            result=sample_result_basic,
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
    def test_create_analysis_charts_partial_success(self, mock_metrics, mock_error, mock_coverage, sample_result_basic):
        """
        Тест, который проверяет создание графиков 
        при частичном успехе
        """
        mock_coverage.return_value = "/path/coverage.png"
        mock_error.return_value = None  # ошибка при создании
        mock_metrics.return_value = "/path/metrics.png"
        
        charts = create_analysis_charts(
            result=sample_result_basic,
            layout_name="test_layout",
            file_path="/test/path.txt"
        )
        
        assert len(charts) == 2
        assert None not in charts
    
    @patch('make_export_plot._create_coverage_pie_chart')
    @patch('make_export_plot._create_error_distribution_chart')
    @patch('make_export_plot._create_metrics_comparison_chart')
    def test_create_analysis_charts_minimal_data(self, mock_metrics, mock_error, mock_coverage, sample_result_minimal):
        """
        Тест, который проверяет создание графиков 
        с минимальными корректными данными
        """
        mock_coverage.return_value = "/path/coverage.png"
        mock_error.return_value = "/path/error.png"
        mock_metrics.return_value = "/path/metrics.png"
        
        charts = create_analysis_charts(
            result=sample_result_minimal,
            layout_name="minimal_layout",
            file_path="/test/path.txt"
        )
        
        assert isinstance(charts, list)
        assert mock_coverage.called
        assert mock_error.called
        assert mock_metrics.called