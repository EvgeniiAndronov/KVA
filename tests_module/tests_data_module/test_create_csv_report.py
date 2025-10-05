import pytest
import os
import tempfile
import csv
from unittest.mock import patch, Mock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'data_module'))
from make_export_file import create_csv_report

class TestCreateCSVReport:
    
    def test_create_csv_report_success(self, temp_dir, sample_result_basic):
        """
        Тест, который проверяет успешное создание 
        CSV отчета
        """
        file_path = create_csv_report(
            result=sample_result_basic,
            file_path="/test/path/file.txt",
            layout_name="test_layout",
            output_dir=temp_dir
        )
        
        assert os.path.exists(file_path)
        assert file_path.endswith('.csv')
        
        # Проверяем содержимое файла
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "ОСНОВНАЯ СТАТИСТИКА" in content
            assert "test_layout" in content
            assert "100" in content  # total_errors
    
    def test_create_csv_report_empty_unknown_chars(self, temp_dir, sample_result_no_errors):
        """
        Тест, который проверяет создание отчета без 
        неизвестных символов
        """
        file_path = create_csv_report(
            result=sample_result_no_errors,
            file_path="/test/path/file.txt",
            layout_name="empty_layout",
            output_dir=temp_dir
        )
        
        assert os.path.exists(file_path)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "НЕИЗВЕСТНЫЕ СИМВОЛЫ" not in content
            assert "ОТЛИЧНО" in content  # оценка качества
    
    def test_create_csv_report_directory_creation(self, temp_dir, sample_result_basic):
        """
        Тест, который проверяет создание директории 
        если её нет
        """
        new_dir = os.path.join(temp_dir, "new_subdir")
        
        file_path = create_csv_report(
            result=sample_result_basic,
            file_path="/test/path/file.txt",
            layout_name="test_layout",
            output_dir=new_dir
        )
        
        assert os.path.exists(new_dir)
        assert os.path.exists(file_path)