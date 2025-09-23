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
    """Тесты для функции create_csv_report"""
    
    def test_create_csv_report_success(self):
        """Тест успешного создания CSV отчета"""
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
            
            file_path = create_csv_report(
                result=sample_result,
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
                assert "1500" in content  # total_errors
    
    def test_create_csv_report_empty_unknown_chars(self):
        """Тест создания отчета без неизвестных символов"""
        with tempfile.TemporaryDirectory() as temp_dir:
            sample_result = {
                'total_errors': 0,
                'total_words': 100,
                'total_characters': 500,
                'processed_characters': 500,
                'unknown_characters': set(),
                'avg_errors_per_word': 0.0,
                'avg_errors_per_char': 0.0,
                'text_type': 'words'
            }
            
            file_path = create_csv_report(
                result=sample_result,
                file_path="/test/path/file.txt",
                layout_name="empty_layout",
                output_dir=temp_dir
            )
            
            assert os.path.exists(file_path)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                assert "НЕИЗВЕСТНЫЕ СИМВОЛЫ" not in content
                assert "ОТЛИЧНО" in content  # оценка качества
    
    def test_create_csv_report_directory_creation(self):
        """Тест создания директории если её нет"""
        with tempfile.TemporaryDirectory() as temp_dir:
            new_dir = os.path.join(temp_dir, "new_subdir")
            
            sample_result = {
                'total_errors': 100,
                'total_words': 50,
                'total_characters': 200,
                'processed_characters': 200,
                'unknown_characters': set(),
                'avg_errors_per_word': 2.0,
                'avg_errors_per_char': 0.01,
                'text_type': 'words'
            }
            
            file_path = create_csv_report(
                result=sample_result,
                file_path="/test/path/file.txt",
                layout_name="test_layout",
                output_dir=new_dir
            )
            
            assert os.path.exists(new_dir)
            assert os.path.exists(file_path)