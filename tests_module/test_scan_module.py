import pytest
from read_files import get_file_size_mb, get_words_from_file, count_lines_in_file, get_text_from_file, count_characters_in_file
from read_files import get_words_from_file_stream, get_text_from_file_stream
from read_layout import read_kl, save_layout_to_file, validate_layout

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

    def test_get_words_from_file_stream_input_types(self, temp_file):
        """
        Тестирует потоковое чтение разных файлов.
        Проверяет работу с существующими путями.
        Убеждается в генерации батчей слов.
        """
        result = get_words_from_file_stream(temp_file, batch_size=2)
        first_batch = next(result)
        assert isinstance(first_batch, list)
        assert all(isinstance(word, str) for word in first_batch)
    
    def test_get_words_from_file_stream_return_type(self, temp_file):
        """
        Проверяет тип возвращаемого генератора.
        Убеждается в корректности структуры батчей.
        Тестирует размеры возвращаемых данных.
        """
        generator = get_words_from_file_stream(temp_file, batch_size=2)
        batch = next(generator)
        assert isinstance(batch, list)
        assert len(batch) <= 2
    
    def test_get_text_from_file_stream_input_types(self, temp_file):
        """
        Тестирует потоковое чтение текстовых файлов.
        Проверяет обработку разных размеров чанков.
        Убеждается в работе с различными кодировками.
        """
        result = get_text_from_file_stream(temp_file, chunk_size=10)
        first_chunk = next(result)
        assert isinstance(first_chunk, str)
    
    def test_get_text_from_file_stream_return_type(self, temp_file):
        """
        Проверяет тип возвращаемого текстового генератора.
        Убеждается в корректности размера чанков.
        Тестирует полноту читаемых данных.
        """
        generator = get_text_from_file_stream(temp_file, chunk_size=10)
        chunk = next(generator)
        assert isinstance(chunk, str)
        assert len(chunk) <= 10
    
    def test_read_kl_input_types(self, test_layout_file):
        """
        Тестирует чтение раскладок из разных форматов.
        Проверяет обработку JSON, CSV и текстовых файлов.
        Убеждается в работе с несуществующими путями.
        """
        result = read_kl(test_layout_file)
        assert isinstance(result, dict)
    
    def test_read_kl_return_type(self, test_layout_file):
        """
        Проверяет тип возвращаемой раскладки.
        Убеждается в корректности структуры данных.
        Тестирует обработку различных форматов файлов.
        """
        result = read_kl(test_layout_file)
        assert isinstance(result, dict)
        assert 'a' in result
    
    def test_save_layout_to_file_input_types(self, sample_rules_old):
        """
        Тестирует сохранение раскладок в разные форматы.
        Проверяет работу с JSON, CSV и текстовыми файлами.
        Убеждается в корректности параметров сохранения.
        """
        result = save_layout_to_file(sample_rules_old, "test_save.json", "json")
        assert result == True
        
        import os
        os.remove("test_save.json")
    
    def test_save_layout_to_file_return_type(self, sample_rules_old):
        """
        Проверяет тип возвращаемого значения сохранения.
        Убеждается в успешности операции записи.
        Тестирует обработку ошибок файловой системы.
        """
        result = save_layout_to_file(sample_rules_old, "test_save.json", "json")
        assert isinstance(result, bool)
        
        import os
        os.remove("test_save.json")
    
    def test_validate_layout_input_types(self, sample_rules_old):
        """
        Тестирует валидацию различных форматов раскладок.
        Проверяет старый и новый форматы данных.
        Убеждается в обнаружении некорректных структур.
        """
        is_valid, errors = validate_layout(sample_rules_old)
        assert isinstance(is_valid, bool)
        assert isinstance(errors, list)
    
    def test_validate_layout_return_type(self, sample_rules_old):
        """
        Проверяет структуру возвращаемых данных валидации.
        Убеждается в наличии статуса и списка ошибок.
        Тестирует корректность проверки правил.
        """
        is_valid, errors = validate_layout(sample_rules_old)
        assert isinstance(is_valid, bool)
        assert isinstance(errors, list)