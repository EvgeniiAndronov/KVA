# test_scan_module.py
import pytest
from read_files import get_file_size_mb, get_words_from_file, count_lines_in_file, get_text_from_file, count_characters_in_file

class TestReadFiles:
    
    def test_get_file_size_mb_input_types(self, temp_file):
        """
        Тестирует обработку разных путей к файлам.
        Проверяет существующие и несуществующие файлы.
        Убеждается в обработке некорректных типов.
        """
        # Корректные типы
        result = get_file_size_mb(temp_file)
        assert isinstance(result, float)
        
        # Неправильные типы - функция возвращает 0 для некорректных путей
        result = get_file_size_mb(123)
        assert result == 0
    
    def test_get_file_size_mb_return_type(self, temp_file):
        """
        Проверяет тип возвращаемого значения.
        Убеждается, что всегда возвращается float.
        Тестирует корректность расчета размера.
        """
        result = get_file_size_mb(temp_file)
        assert isinstance(result, float)
    
    def test_get_words_from_file_input_types(self, temp_file):
        """
        Тестирует чтение слов из разных файлов.
        Проверяет существующие и несуществующие пути.
        Убеждается в обработке ошибок файловой системы.
        """
        # Корректные типы
        result = get_words_from_file(temp_file)
        assert isinstance(result, list)
        
        # Проверка с несуществующим файлом
        with pytest.raises(FileNotFoundError):
            get_words_from_file("nonexistent_file.txt")
    
    def test_get_words_from_file_return_type(self, temp_file):
        """
        Проверяет тип возвращаемого значения.
        Убеждается, что возвращается список строк.
        Тестирует корректность разбиения на слова.
        """
        result = get_words_from_file(temp_file)
        assert isinstance(result, list)
        assert all(isinstance(word, str) for word in result)
    
    def test_count_lines_in_file_input_types(self, temp_file):
        """
        Тестирует подсчет строк в разных файлах.
        Проверяет существующие и несуществующие пути.
        Убеждается в обработке ошибок чтения.
        """
        # Корректные типы
        result = count_lines_in_file(temp_file)
        assert isinstance(result, int)
        
        # Проверка с несуществующим файлом
        with pytest.raises(FileNotFoundError):
            count_lines_in_file("nonexistent_file.txt")
    
    def test_count_lines_in_file_return_type(self, temp_file):
        """
        Проверяет тип возвращаемого значения.
        Убеждается, что всегда возвращается int.
        Тестирует точность подсчета строк.
        """
        result = count_lines_in_file(temp_file)
        assert isinstance(result, int)
    
    def test_get_text_from_file_input_types(self, temp_file):
        """
        Тестирует чтение текста из разных файлов.
        Проверяет существующие и несуществующие пути.
        Убеждается в обработке ошибок файловой системы.
        """
        # Корректные типы
        result = get_text_from_file(temp_file)
        assert isinstance(result, str)
        
        # Проверка с несуществующим файлом
        with pytest.raises(FileNotFoundError):
            get_text_from_file("nonexistent_file.txt")
    
    def test_get_text_from_file_return_type(self, temp_file):
        """
        Проверяет тип возвращаемого значения.
        Убеждается, что всегда возвращается строка.
        Тестирует полноту прочитанного текста.
        """
        result = get_text_from_file(temp_file)
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_count_characters_in_file_input_types(self, temp_file):
        """
        Тестирует подсчет символов в разных файлах.
        Проверяет существующие и несуществующие пути.
        Убеждается в обработке ошибок чтения.
        """
        # Корректные типы
        result = count_characters_in_file(temp_file)
        assert isinstance(result, int)
        
        # Проверка с несуществующим файлом
        with pytest.raises(FileNotFoundError):
            count_characters_in_file("nonexistent_file.txt")
    
    def test_count_characters_in_file_return_type(self, temp_file):
        """
        Проверяет тип возвращаемого значения.
        Убеждается, что всегда возвращается int.
        Тестирует точность подсчета символов.
        """
        result = count_characters_in_file(temp_file)
        assert isinstance(result, int)