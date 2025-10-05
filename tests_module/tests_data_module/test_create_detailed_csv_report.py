import pytest
import os
import tempfile
import csv
from datetime import datetime
from unittest.mock import patch, Mock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'data_module'))
from make_export_file import create_detailed_csv_report

class TestCreateDetailedCSVReport:
    
    def test_create_detailed_csv_report_success(self, temp_dir, sample_results_list):
        """
        Тест, который проверяет успешное создание 
        детального CSV отчета
        """
        file_path = create_detailed_csv_report(
            results_list=sample_results_list,
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
    
    def test_create_detailed_csv_report_empty_list(self, temp_dir):
        """
        Тест, который проверяет создание отчета с 
        пустым списком результатов
        """
        file_path = create_detailed_csv_report(
            results_list=[],
            output_dir=temp_dir
        )
        
        assert os.path.exists(file_path)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            assert len(rows) == 1  # только заголовок
    
    def test_create_detailed_csv_report_missing_fields(self, temp_dir):
        """
        Тест, который проверяет обработку неполных 
        данных в результатах
        """
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
    
    @patch('make_export_file._get_quality_assessment')
    def test_create_detailed_csv_report_quality_assessment_called(self, mock_quality, temp_dir, sample_results_list):
        """
        Тест, который проверяет вызов функции оценки качества
        """
        mock_quality.return_value = "ТЕСТОВАЯ_ОЦЕНКА"
        
        file_path = create_detailed_csv_report(
            results_list=sample_results_list,
            output_dir=temp_dir
        )
        
        assert os.path.exists(file_path)
        # Проверяем, что функция оценки качества была вызвана
        assert mock_quality.called
        
        # Проверяем, что тестовая оценка попала в CSV
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "ТЕСТОВАЯ_ОЦЕНКА" in content