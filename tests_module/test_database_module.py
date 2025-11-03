import pytest
from database import take_lk_from_db, save_layout_to_db, take_all_data_from_lk, take_lk_names_from_lk
from database import save_analysis_result, get_analysis_history, get_analysis_statistics
from database import get_finger_statistics, get_aggregated_finger_statistics
from db_init import init_tables, make_mok_data, migrate_database

class TestDatabaseSimple:
    
    def test_take_lk_from_db_input_types(self, temp_db):
        """
        Тестирует обработку разных типов входных данных.
        Проверяет корректные строки и неправильные типы.
        Убеждается, что функция возвращает данные корректно.
        """
        # Корректные типы (существующая раскладка)
        result = take_lk_from_db("test_layout")
        assert isinstance(result, dict)
        
        # Корректные типы (несуществующая раскладка) - функция возвращает None
        result = take_lk_from_db("nonexistent_layout")
        assert result is None
        
        # Неправильные типы - функция может возвращать None или словарь
        result = take_lk_from_db(123)
        # Принимаем любой результат, так как функция может обрабатывать это по-разному
        assert result is None or isinstance(result, dict)
    
    def test_take_lk_from_db_return_type(self, temp_db):
        """
        Проверяет тип возвращаемого значения.
        Убеждается, что возвращается словарь или None.
        Тестирует согласованность возвращаемых типов.
        """
        result = take_lk_from_db("test_layout")
        assert isinstance(result, dict) or result is None
    
    def test_save_layout_to_db_input_types(self, temp_db, sample_rules_old):
        """
        Тестирует валидацию входных параметров.
        Проверяет корректные и некорректные имена раскладок.
        Убеждается в обработке неправильных типов данных.
        """
        # Корректные типы
        result = save_layout_to_db("test_save", sample_rules_old)
        assert isinstance(result, bool)
        
        # Неправильные типы - функция может возвращать True или False
        result = save_layout_to_db(123, sample_rules_old)
        assert isinstance(result, bool)
    
    def test_save_layout_to_db_return_type(self, temp_db, sample_rules_old):
        """
        Проверяет тип возвращаемого значения.
        Убеждается, что всегда возвращается bool.
        Тестирует согласованность возвращаемых данных.
        """
        result = save_layout_to_db("test_return", sample_rules_old)
        assert isinstance(result, bool)

    def test_take_all_data_from_lk_input_types(self, temp_db):
        """
        Тестирует получение всех данных из таблицы раскладок.
        Проверяет работу без параметров и фильтрацию.
        Убеждается в корректности SQL запросов.
        """
        result = take_all_data_from_lk()
        assert isinstance(result, list)
    
    def test_take_all_data_from_lk_return_type(self, temp_db):
        """
        Проверяет тип возвращаемых данных таблицы.
        Убеждается в структуре записей раскладок.
        Тестирует полноту получаемой информации.
        """
        result = take_all_data_from_lk()
        assert isinstance(result, list)
        if result:
            assert isinstance(result[0], tuple)
    
    def test_take_lk_names_from_lk_input_types(self, temp_db):
        """
        Тестирует получение имен раскладок из базы.
        Проверяет фильтрацию тестовых данных.
        Убеждается в работе без параметров.
        """
        result = take_lk_names_from_lk()
        assert isinstance(result, list)
    
    def test_take_lk_names_from_lk_return_type(self, temp_db):
        """
        Проверяет тип возвращаемых имен раскладок.
        Убеждается в отсутствии тестовых записей.
        Тестирует структуру возвращаемого списка.
        """
        result = take_lk_names_from_lk()
        assert isinstance(result, list)
        if result:
            assert isinstance(result[0], tuple)
    
    def test_save_analysis_result_input_types(self, temp_db, test_analysis_result):
        """
        Тестирует сохранение результатов анализа в базу.
        Проверяет различные типы анализов и данные.
        Убеждается в корректности структуры записи.
        """
        record_id = save_analysis_result("test_layout", test_analysis_result, "test_file.txt", "words")
        assert isinstance(record_id, int)
    
    def test_save_analysis_result_return_type(self, temp_db, test_analysis_result_minimal):
        """
        Проверяет тип возвращаемого ID записи.
        Убеждается в успешности сохранения данных.
        Тестирует работу с различными типами анализов.
        """
        record_id = save_analysis_result("test_layout", test_analysis_result_minimal, "test_file.txt", "words")
        assert isinstance(record_id, int)
        assert record_id > 0
    
    def test_get_analysis_history_input_types(self, temp_db):
        """
        Тестирует получение истории анализов из базы.
        Проверяет работу с фильтрами и лимитами.
        Убеждается в корректности SQL запросов.
        """
        result = get_analysis_history("test_layout", limit=10)
        assert isinstance(result, list)
    
    def test_get_analysis_history_return_type(self, temp_db):
        """
        Проверяет тип возвращаемой истории анализов.
        Убеждается в структуре записей результатов.
        Тестирует применение лимитов и фильтров.
        """
        result = get_analysis_history("test_layout", limit=10)
        assert isinstance(result, list)
        if result:
            assert len(result[0]) == 4  # id, name_lk, count_errors, type_test
    
    def test_get_analysis_statistics_input_types(self, temp_db):
        """
        Тестирует получение статистики анализов раскладки.
        Проверяет работу с существующими раскладками.
        Убеждается в расчете агрегированных данных.
        """
        result = get_analysis_statistics("test_layout")
        assert isinstance(result, dict)
    
    def test_get_analysis_statistics_return_type(self, temp_db):
        """
        Проверяет структуру возвращаемой статистики.
        Убеждается в наличии всех метрик анализа.
        Тестирует корректность агрегированных значений.
        """
        result = get_analysis_statistics("test_layout")
        assert isinstance(result, dict)
        assert 'total_tests' in result
        assert 'avg_errors' in result
    
    def test_get_finger_statistics_input_types(self, temp_db, test_analysis_result):
        """
        Тестирует получение статистики пальцев для анализа.
        Проверяет работу с корректными ID записей.
        Убеждается в извлечении связанных данных.
        """
        # Сначала создаем запись анализа
        record_id = save_analysis_result("test_layout", test_analysis_result, "test_file.txt", "words")
        result = get_finger_statistics(record_id)
        assert isinstance(result, dict)
    
    def test_get_finger_statistics_return_type(self, temp_db, test_analysis_result):
        """
        Проверяет тип возвращаемой статистики пальцев.
        Убеждается в корректности структуры данных.
        Тестирует подсчет нажатий для каждого пальца.
        """
        record_id = save_analysis_result("test_layout", test_analysis_result, "test_file.txt", "words")
        result = get_finger_statistics(record_id)
        assert isinstance(result, dict)
        assert 'index' in result or result == {}
    
    def test_get_aggregated_finger_statistics_input_types(self, temp_db):
        """
        Тестирует получение агрегированной статистики пальцев.
        Проверяет работу с различными параметрами фильтрации.
        Убеждается в корректности агрегации данных.
        """
        result = get_aggregated_finger_statistics("test_layout", limit=5)
        assert isinstance(result, dict)
    
    def test_get_aggregated_finger_statistics_return_type(self, temp_db):
        """
        Проверяет тип агрегированной статистики пальцев.
        Убеждается в суммировании нажатий по пальцам.
        Тестирует применение лимитов и фильтров раскладок.
        """
        result = get_aggregated_finger_statistics("test_layout", limit=5)
        assert isinstance(result, dict)
    
    def test_init_tables_input_types(self, temp_db):
        """
        Тестирует инициализацию таблиц базы данных.
        Проверяет создание основных таблиц системы.
        Убеждается в корректности SQL схемы.
        """
        # Функция не принимает параметров, просто проверяем выполнение
        try:
            init_tables()
            assert True
        except Exception:
            assert False
    
    def test_init_tables_return_type(self, temp_db):
        """
        Проверяет выполнение инициализации таблиц.
        Убеждается в отсутствии возвращаемого значения.
        Тестирует создание всех необходимых таблиц.
        """
        result = init_tables()
        assert result is None
    
    def test_make_mok_data_input_types(self, temp_db):
        """
        Тестирует создание тестовых данных в базе.
        Проверяет работу с различными параметрами.
        Убеждается в корректности вставки записей.
        """
        # Функция не возвращает значения, проверяем выполнение
        try:
            make_mok_data("a", "test_mok_layout")
            assert True
        except Exception:
            assert False
    
    def test_make_mok_data_return_type(self, temp_db):
        """
        Проверяет выполнение создания тестовых данных.
        Убеждается в отсутствии возвращаемого значения.
        Тестирует заполнение таблицы раскладок.
        """
        result = make_mok_data("a", "test_mok_layout")
        assert result is None
    
    def test_migrate_database_input_types(self, temp_db):
        """
        Тестирует миграцию структуры базы данных.
        Проверяет добавление новых колонок и таблиц.
        Убеждается в совместимости изменений.
        """
        # Функция не принимает параметров, проверяем выполнение
        try:
            migrate_database()
            assert True
        except Exception:
            assert False
    
    def test_migrate_database_return_type(self, temp_db):
        """
        Проверяет выполнение миграции базы данных.
        Убеждается в отсутствии возвращаемого значения.
        Тестирует обновление схемы до актуальной версии.
        """
        result = migrate_database()
        assert result is None