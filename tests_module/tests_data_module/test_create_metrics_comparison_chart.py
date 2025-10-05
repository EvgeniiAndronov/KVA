import pytest
import os
import tempfile
from unittest.mock import patch, Mock, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'data_module'))
from make_export_plot import _create_metrics_comparison_chart

class TestCreateMetricsComparisonChart:
    
    @patch('make_export_plot.plt.savefig')
    @patch('make_export_plot.plt.subplot')
    @patch('make_export_plot.plt.figure')
    @patch('make_export_plot.plt.close')
    def test_create_metrics_comparison_chart_success(self, mock_close, mock_figure, mock_subplot, mock_savefig, temp_dir, sample_result_basic):
        """
        Тест, который проверяет успешное 
        создание радарной диаграммы
        """
        # Мокаем весь процесс создания графика
        mock_fig = MagicMock()
        mock_ax = MagicMock()
        
        mock_figure.return_value = mock_fig
        mock_subplot.return_value = mock_ax
        
        # Мокаем успешное сохранение файла
        def mock_savefig_side_effect(filepath, **kwargs):
            # Создаем пустой файл для эмуляции сохранения
            open(filepath, 'w').close()
            return None
        
        mock_savefig.side_effect = mock_savefig_side_effect
        
        file_path = _create_metrics_comparison_chart(
            result=sample_result_basic,
            layout_name="test_layout",
            timestamp="20240101_120000",
            output_dir=temp_dir
        )
        
        # Проверяем что функция вернула путь
        assert file_path is not None
        assert file_path.endswith('.png')
        assert "metrics_radar" in file_path
        
        # Проверяем что файл был создан
        assert os.path.exists(file_path)
        
        # Проверяем что методы matplotlib были вызваны
        assert mock_figure.called
        assert mock_subplot.called
        assert mock_savefig.called
        assert mock_close.called
    
    @patch('make_export_plot.plt.savefig')
    @patch('make_export_plot.plt.subplot')
    @patch('make_export_plot.plt.figure')
    @patch('make_export_plot.plt.close')
    def test_create_metrics_comparison_chart_high_errors(self, mock_close, mock_figure, mock_subplot, mock_savefig, temp_dir, sample_result_high_errors):
        """
        Тест, который проверяет создание 
        диаграммы с высоким уровнем ошибок
        """
        # Мокаем процесс создания графика
        mock_fig = MagicMock()
        mock_ax = MagicMock()
        
        mock_figure.return_value = mock_fig
        mock_subplot.return_value = mock_ax
        
        def mock_savefig_side_effect(filepath, **kwargs):
            open(filepath, 'w').close()
            return None
        
        mock_savefig.side_effect = mock_savefig_side_effect
        
        file_path = _create_metrics_comparison_chart(
            result=sample_result_high_errors,
            layout_name="high_error_layout",
            timestamp="20240101_120000",
            output_dir=temp_dir
        )
        
        assert file_path is not None
        assert os.path.exists(file_path)
    
    @patch('make_export_plot.plt.subplot')
    def test_create_metrics_comparison_chart_exception(self, mock_subplot, temp_dir, sample_result_basic):
        """
        Тест, который проверяет обработку исключения 
        при создании радарной диаграммы
        """
        mock_subplot.side_effect = Exception("Plot error")
        
        file_path = _create_metrics_comparison_chart(
            result=sample_result_basic,
            layout_name="test_layout",
            timestamp="20240101_120000",
            output_dir=temp_dir
        )
        
        assert file_path is None
    
    @patch('make_export_plot.plt.savefig')
    @patch('make_export_plot.plt.subplot')
    @patch('make_export_plot.plt.figure')
    def test_create_metrics_comparison_chart_save_error(self, mock_figure, mock_subplot, mock_savefig, temp_dir, sample_result_basic):
        """
        Тест, который проверяет обработку ошибки сохранения файла
        """
        # Мокаем создание графика
        mock_fig = MagicMock()
        mock_ax = MagicMock()
        
        mock_figure.return_value = mock_fig
        mock_subplot.return_value = mock_ax
        
        # Мокаем ошибку при сохранении
        mock_savefig.side_effect = Exception("Save error")
        
        file_path = _create_metrics_comparison_chart(
            result=sample_result_basic,
            layout_name="test_layout",
            timestamp="20240101_120000",
            output_dir=temp_dir
        )
        
        # Функция должна вернуть None при ошибке сохранения
        assert file_path is None