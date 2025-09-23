import pytest
import os
import tempfile
import csv
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'data_module'))
from make_export_file import create_detailed_csv_report

class TestCreateDetailedCSVReport:
    """Тесты для функции create_detailed_csv_report"""
    
    def test_create_detailed_csv_report_success(self):
        """Тест успешного создания детального отчета"""
        with tempfile.TemporaryDirectory() as temp_dir:
            results_list = [
                {
                    'result': {
                        'total_errors': 100,
                        'total_words': 50,
                        'total_characters': 200,
                        'processed_characters': 180,
                        'unknown_characters': {'@'},
                        'avg_errors_per_word': 2.0,
                        'avg_errors_per_char': 0.01,
                        'text_type': 'words'
                    },
                    'file_path': '/path/to/file1.txt',
                    'layout_name': 'layout1',
                    'timestamp': '2024-01-01 10:00:00'
                },
                {
                    'result': {
                        'total_errors': 50,
                        'total_words': 60,
                        'total_characters': 250,
                        'processed_characters': 240,
                        'unknown_characters': {'#'},
                        'avg_errors_per_word': 0.83,
                        'avg_errors_per_char': 0.002,
                        'text_type': 'words'
                    },
                    'file_path': '/path/to/file2.txt',
                    'layout_name': 'layout2',
                    'timestamp': '2024-01-01 11:00:00'
                }
            ]
            
            file_path = create_detailed_csv_report(
                results_list=results_list,
                output_dir=temp_dir
            )
            
            assert os.path.exists(file_path)
            
            # Проверяем структуру CSV
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)
                
                assert len(rows) == 3  # заголовок + 2 строки данных
                assert rows[0] == ["Файл", "Раскладка", "Тип анализа", "Дата", "Общие ошибки", 
                                 "Слова", "Символы", "Обработано символов", "Ошибок/слово", 
                                 "Ошибок/символ", "Покрытие %", "Неизвестных символов", "Оценка качества"]
                assert rows[1][1] == 'layout1'
                assert rows[2][1] == 'layout2'
    
    def test_create_detailed_csv_report_empty_list(self):
        """Тест с пустым списком результатов"""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = create_detailed_csv_report(
                results_list=[],
                output_dir=temp_dir
            )
            
            assert os.path.exists(file_path)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)
                assert len(rows) == 1  # только заголовок
    
    def test_create_detailed_csv_report_missing_fields(self):
        """Тест с неполными данными в результатах"""
        with tempfile.TemporaryDirectory() as temp_dir:
            results_list = [
                {
                    'result': {
                        'total_errors': 100,
                        'total_words': 50,
                        'total_characters': 200,
                        'processed_characters': 180,
                        'unknown_characters': {'@'},
                        'avg_errors_per_word': 2.0,
                        'avg_errors_per_char': 0.01,
                        'text_type': 'words'
                    }
                    # отсутствуют file_path, layout_name, timestamp
                }
            ]
            
            file_path = create_detailed_csv_report(
                results_list=results_list,
                output_dir=temp_dir
            )
            
            assert os.path.exists(file_path)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)
                assert rows[1][0] == 'N/A'  # file_path
                assert rows[1][1] == 'N/A'  # layout_name