import pytest
import sqlite3
from unittest.mock import Mock, patch, MagicMock
from database import take_lk_from_db


class TestTakeLkFromDb:
    """Тесты для функции take_lk_from_db"""
    
    def test_successful_data_retrieval(self):
        """Тест успешного получения данных раскладки"""
        # Мокируем тестовые данные (больше 10 записей)
        test_data = [
            ('a', 1), ('b', 2), ('c', 3), ('d', 4), ('e', 5),
            ('f', 6), ('g', 7), ('h', 8), ('i', 9), ('j', 10),
            ('k', 11), ('l', 12)  # > 10 записей
        ]
        
        with patch('database.sqlite3.connect') as mock_connect:
            # Настраиваем моки
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchall.return_value = test_data
            
            # Вызываем тестируемую функцию
            result = take_lk_from_db('test_layout')
            
            # Проверяем правильность вызовов
            mock_connect.assert_called_once_with("database.db")
            mock_cursor.execute.assert_called_once_with(
                "select letter, error from lk where name_lk = ?", 
                ('test_layout',)
            )
            mock_conn.commit.assert_called_once()
            mock_conn.close.assert_called_once()
            
            # Проверяем результат
            expected_result = {
                'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5,
                'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 10,
                'k': 11, 'l': 12
            }
            assert result == expected_result
    
    def test_insufficient_data_returns_none(self):
        """Тест возврата None при недостаточном количестве данных"""
        # Мокируем тестовые данные (меньше или равно 10 записей)
        test_data = [('a', 1), ('b', 2), ('c', 3)]  # < 10 записей
        
        with patch('database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchall.return_value = test_data
            
            result = take_lk_from_db('test_layout')
            
            # Проверяем, что функция возвращает None
            assert result is None
            mock_conn.close.assert_called_once()
    
    def test_exactly_10_records_returns_none(self):
        """Тест возврата None при точном количестве 10 записей"""
        # Мокируем ровно 10 записей
        test_data = [('a', i) for i in range(10)]
        
        with patch('database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchall.return_value = test_data
            
            result = take_lk_from_db('test_layout')
            
            assert result is None
    
    def test_empty_result_returns_none(self):
        """Тест возврата None при пустом результате"""
        with patch('database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchall.return_value = []  # Пустой результат
            
            result = take_lk_from_db('nonexistent_layout')
            
            assert result is None
    
    def test_database_connection_parameters(self):
        """Тест правильности параметров соединения с БД"""
        with patch('database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchall.return_value = [('a', 1), ('b', 2)]
            
            take_lk_from_db('test_layout')
            
            # Проверяем, что соединение создается с правильной базой
            mock_connect.assert_called_once_with("database.db")
    
    def test_sql_query_parameters(self):
        """Тест правильности параметров SQL-запроса"""
        with patch('database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchall.return_value = [('a', 1), ('b', 2)]
            
            layout_name = "russian_layout"
            take_lk_from_db(layout_name)
            
            # Проверяем, что запрос выполняется с правильными параметрами
            mock_cursor.execute.assert_called_once_with(
                "select letter, error from lk where name_lk = ?", 
                (layout_name,)
            )
    
    @pytest.mark.parametrize("test_data,expected", [
        # Больше 10 записей - должен вернуть словарь
        ([('a', i) for i in range(15)], {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 
                                        'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9,
                                        'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14}),
        # Ровно 11 записей - должен вернуть словарь
        ([(chr(97 + i), i) for i in range(11)], 
         {chr(97 + i): i for i in range(11)}),
        # Ровно 10 записей - должен вернуть None
        ([(chr(97 + i), i) for i in range(10)], None),
        # 9 записей - должен вернуть None
        ([(chr(97 + i), i) for i in range(9)], None),
    ])
    def test_various_data_sizes(self, test_data, expected):
        """Параметризованный тест для различных размеров данных"""
        with patch('database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchall.return_value = test_data
            
            result = take_lk_from_db('test_layout')
            
            assert result == expected


# Интеграционные тесты с реальной БД в памяти
class TestTakeLkFromDbIntegration:
    """Интеграционные тесты с реальной базой данных"""
    
    @pytest.fixture
    def memory_db(self):
        """Создает базу данных в памяти с тестовыми таблицами"""
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        
        # Создаем тестовую таблицу
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lk (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name_lk TEXT NOT NULL,
                letter TEXT NOT NULL,
                error INTEGER
            )
        """)
        
        yield conn, cursor
        conn.close()
    
    def test_integration_with_real_db_success(self, memory_db):
        """Интеграционный тест с реальной БД - успешный сценарий"""
        conn, cursor = memory_db
        
        # Добавляем тестовые данные (> 10 записей)
        layout_name = "russian_test"
        for i in range(15):
            letter = chr(ord('а') + i)  # Русские буквы
            cursor.execute(
                "INSERT INTO lk (name_lk, letter, error) VALUES (?, ?, ?)",
                (layout_name, letter, i)
            )
        conn.commit()
        
        # Тестируем функцию с подменой соединения
        with patch('database.sqlite3.connect', return_value=conn):
            result = take_lk_from_db(layout_name)
            
            # Проверяем результат
            assert result is not None
            assert len(result) == 15
            for i in range(15):
                expected_letter = chr(ord('а') + i)
                assert result[expected_letter] == i
    
    def test_integration_with_real_db_insufficient_data(self, memory_db):
        """Интеграционный тест с реальной БД - недостаточно данных"""
        conn, cursor = memory_db
        
        # Добавляем только 5 записей
        layout_name = "small_layout"
        for i in range(5):
            cursor.execute(
                "INSERT INTO lk (name_lk, letter, error) VALUES (?, ?, ?)",
                (layout_name, chr(ord('a') + i), i)
            )
        conn.commit()
        
        with patch('database.sqlite3.connect', return_value=conn):
            result = take_lk_from_db(layout_name)
            
            # Должен вернуть None, так как данных меньше 10
            assert result is None


# Тесты для обработки крайних случаев
class TestTakeLkFromDbEdgeCases:
    """Тесты для крайних случаев"""
    
    def test_special_characters_in_layout_name(self):
        """Тест с специальными символами в имени раскладки"""
        test_data = [('a', 1), ('b', 2)]  # Мало данных для возврата None
        
        with patch('database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchall.return_value = test_data
            
            # Тестируем с различными специальными именами
            special_names = [
                "layout with spaces",
                "layout-with-dashes",
                "layout_with_underscores",
                "LayoutWithCaps",
                "layout123",
                "layout@special#chars"
            ]
            
            for name in special_names:
                take_lk_from_db(name)
                # Проверяем, что имя правильно передается в запрос
                mock_cursor.execute.assert_called_with(
                    "select letter, error from lk where name_lk = ?", 
                    (name,)
                )
    
    def test_unicode_characters(self):
        """Тест с Unicode-символами"""
        test_data = [('α', 1), ('β', 2), ('γ', 3)]  # Греческие буквы
        
        with patch('database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchall.return_value = test_data
            
            result = take_lk_from_db('greek_layout')
            
            # Должен вернуть None, так как данных меньше 10
            assert result is None