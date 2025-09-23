import pytest
import os
import tempfile
import csv
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'data_module'))
from make_export_file import export_unknown_characters_csv

class TestExportUnknownCharactersCSV:
    """Тесты для функции export_unknown_characters_csv"""
    
    def test_export_unknown_characters_csv_success(self):
        """Тест успешного экспорта неизвестных символов"""
        with tempfile.TemporaryDirectory() as temp_dir:
            unknown_chars = {'@', '#', '$', '€', '©'}
            
            file_path = export_unknown_characters_csv(
                unknown_chars=unknown_chars,
                layout_name="test_layout",
                output_dir=temp_dir
            )
            
            assert os.path.exists(file_path)
            assert "unknown_chars" in file_path
            
            # Проверяем содержимое
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)
                
                assert len(rows) == 6  # заголовок + 5 символов
                assert rows[0] == ["Символ", "Unicode код", "Описание"]
                
                # Проверяем что символы отсортированы
                symbols = [row[0] for row in rows[1:]]
                assert "'#'" in symbols[0]  # '#' должен быть первым
    
    def test_export_unknown_characters_csv_empty(self):
        """Тест экспорта пустого множества символов"""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = export_unknown_characters_csv(
                unknown_chars=set(),
                layout_name="empty_layout",
                output_dir=temp_dir
            )
            
            assert os.path.exists(file_path)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)
                assert len(rows) == 1  # только заголовок
    
    def test_export_unknown_characters_csv_special_chars(self):
        """Тест экспорта специальных символов"""
        with tempfile.TemporaryDirectory() as temp_dir:
            unknown_chars = {'\n', '\t', ' ', '®'}
            
            file_path = export_unknown_characters_csv(
                unknown_chars=unknown_chars,
                layout_name="special_layout",
                output_dir=temp_dir
            )
            
            assert os.path.exists(file_path)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)
                
                # Проверяем что специальные символы корректно представлены
                symbols = [row[0] for row in rows[1:]]
                assert any("\\n" in symbol for symbol in symbols)  # перенос строки
                assert any("\\t" in symbol for symbol in symbols)  # табуляция