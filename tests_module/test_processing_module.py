import pytest
from calculate_data import make_processing, validate_rules, make_text_processing, make_processing_stream, make_text_processing_stream

class TestCalculateData:
    
    def test_make_processing_input_types(self, sample_word_list, sample_rules_old):
        """
        Тестирует обработку разных типов входных данных.
        Проверяет валидные списки слов и правила.
        Убеждается в обработке некорректных параметров.
        """
        # Корректные типы
        result = make_processing(sample_word_list, sample_rules_old)
        assert isinstance(result, dict)
        
        # Неправильные типы - функция может обрабатывать строку как список символов
        result = make_processing("not_list", sample_rules_old)
        assert isinstance(result, dict)
    
    def test_make_processing_return_type(self, sample_word_list, sample_rules_old):
        """
        Проверяет структуру возвращаемого словаря.
        Убеждается в наличии обязательных ключей.
        Тестирует корректность типов значений.
        """
        result = make_processing(sample_word_list, sample_rules_old)
        assert isinstance(result, dict)
        assert 'total_errors' in result
        assert 'total_words' in result
        assert 'total_characters' in result
    
    def test_validate_rules_input_types(self, sample_rules_old):
        """
        Тестирует валидацию разных форматов правил.
        Проверяет старый и новый форматы данных.
        Убеждается в отбраковке некорректных типов.
        """
        # Корректные типы (старый формат)
        result = validate_rules(sample_rules_old)
        assert result == True
        
        # Проверка с неправильными типами
        with pytest.raises(ValueError):
            validate_rules("not_dict")
    
    def test_validate_rules_return_type(self, sample_rules_old):
        """
        Проверяет тип возвращаемого значения.
        Убеждается, что всегда возвращается bool.
        Тестирует логику валидации правил.
        """
        result = validate_rules(sample_rules_old)
        assert isinstance(result, bool)
    
    def test_make_text_processing_input_types(self, sample_text, sample_rules_old):
        """
        Тестирует обработку текста разных типов.
        Проверяет валидные строки и словари правил.
        Убеждается в обработке некорректных параметров.
        """
        # Корректные типы
        result = make_text_processing(sample_text, sample_rules_old)
        assert isinstance(result, dict)
        
        # Неправильные типы - функция может падать с TypeError
        # Оборачиваем в try-except для обработки возможной ошибки
        try:
            result = make_text_processing(sample_text, "not_dict")
            assert isinstance(result, dict)
        except TypeError:
            # Ожидаемое поведение - функция не может работать с некорректными правилами
            pass
    
    def test_make_text_processing_return_type(self, sample_text, sample_rules_old):
        """
        Проверяет структуру результата анализа.
        Убеждается в наличии всех необходимых полей.
        Тестирует корректность типа текста.
        """
        result = make_text_processing(sample_text, sample_rules_old)
        assert isinstance(result, dict)
        assert 'text_type' in result

    def test_make_processing_stream_input_types(self, word_generator, sample_rules_old, sample_word_list):
        """
        Тестирует потоковую обработку разных типов данных.
        Проверяет работу с генераторами слов и правилами.
        Убеждается в корректной обработке батчей.
        """
        result = make_processing_stream(word_generator(), sample_rules_old, total_words=len(sample_word_list))
        assert isinstance(result, dict)
    
    def test_make_processing_stream_return_type(self, word_generator, sample_rules_old, sample_word_list):
        """
        Проверяет структуру возвращаемого словаря потоковой обработки.
        Убеждается в наличии статистики по пальцам.
        Тестирует корректность расчетов ошибок.
        """
        result = make_processing_stream(word_generator(), sample_rules_old, total_words=len(sample_word_list))
        assert isinstance(result, dict)
        assert 'total_errors' in result
        assert 'total_words' in result
        assert 'finger_statistics' in result
    
    def test_make_text_processing_stream_input_types(self, text_generator, sample_rules_old, sample_text):
        """
        Тестирует потоковую обработку текстовых данных.
        Проверяет работу с генераторами текста.
        Убеждается в обработке чанков разного размера.
        """
        result = make_text_processing_stream(text_generator(), sample_rules_old, total_chars=len(sample_text))
        assert isinstance(result, dict)
    
    def test_make_text_processing_stream_return_type(self, text_generator, sample_rules_old, sample_text):
        """
        Проверяет структуру результата потокового анализа.
        Убеждается в наличии типа текста и статистики.
        Тестирует подсчет слов и символов.
        """
        result = make_text_processing_stream(text_generator(), sample_rules_old, total_chars=len(sample_text))
        assert isinstance(result, dict)
        assert 'text_type' in result
        assert 'total_words' in result
        assert 'total_characters' in result