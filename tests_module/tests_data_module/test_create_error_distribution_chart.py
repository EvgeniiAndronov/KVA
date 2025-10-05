import pytest
import os
import tempfile
from unittest.mock import patch, Mock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'data_module'))
from make_export_plot import _create_error_distribution_chart

class TestCreateErrorDistributionChart:
    
    def test_create_error_distribution_chart_success(self, temp_dir, sample_result_basic):
        """
        Тест, который проверяет успешное создание 
        гистограммы распределения ошибок
        """
        file_path = _create_error_distribution_chart(
            result=sample_result_basic,
            layout_name="test_layout",
            timestamp="20240101_120000",
            output_dir=temp_dir
        )
        
        assert file_path is not None
        assert os.path.exists(file_path)
        assert file_path.endswith('.png')
        assert "error_distribution" in file_path
    
    def test_create_error_distribution_chart_small_values(self, temp_dir, sample_result_minimal):
        """
        Тест, который проверяет создание гистограммы 
        с малыми значениями ошибок
        """
        file_path = _create_error_distribution_chart(
            result=sample_result_minimal,
            layout_name="small_layout",
            timestamp="20240101_120000",
            output_dir=temp_dir
        )
        
        assert file_path is not None
        assert os.path.exists(file_path)
    
    @patch('make_export_plot.plt.subplots')
    def test_create_error_distribution_chart_exception(self, mock_subplots, sample_result_basic):
        """
        Тест, который проверяет обработку исключения 
        при создании гистограммы
        """
        mock_subplots.side_effect = Exception("Subplots error")
        
        file_path = _create_error_distribution_chart(
            result=sample_result_basic,
            layout_name="test_layout",
            timestamp="20240101_120000",
            output_dir="/tmp"
        )
        
        assert file_path is None