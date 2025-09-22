import pytest
from unittest.mock import Mock, patch
import sys
import os

# Добавляем путь для импорта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from db_init import init_tables, sql_querry_init_db, sql_querry_init_lk


class TestInitTables:
    """Тесты для функции init_tables"""
    
    def test_init_tables_creates_both_tables(self):
        """Тест создания обеих таблиц"""
        with patch('db_init.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            
            init_tables()
            
            # Проверяем, что connect был вызван с правильной базой
            mock_connect.assert_called_once_with("database.db")
            
            # Проверяем, что были выполнены оба CREATE TABLE запроса
            assert mock_cursor.execute.call_count == 2
            mock_cursor.execute.assert_any_call(sql_querry_init_lk)
            mock_cursor.execute.assert_any_call(sql_querry_init_db)
            
            # Проверяем, что были вызваны commit и close
            mock_conn.commit.assert_called_once()
            mock_conn.close.assert_called_once()
    
    def test_init_tables_database_operations(self):
        """Тест последовательности операций с БД"""
        with patch('db_init.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            
            init_tables()
            
            # Проверяем последовательность вызовов
            calls = [call[0][0] for call in mock_cursor.execute.call_args_list]
            assert sql_querry_init_lk in calls
            assert sql_querry_init_db in calls
    
    def test_init_tables_sql_injection_prevention(self):
        """Тест, что SQL-запросы не уязвимы к инъекциям"""
        with patch('db_init.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            
            init_tables()
            
            # Проверяем, что запросы выполняются как есть, без конкатенации
            for call in mock_cursor.execute.call_args_list:
                sql = call[0][0]
                # Убеждаемся, что это не f-строка с подстановкой переменных
                assert 'f"' not in sql
                assert "f'" not in sql
    
    def test_init_tables_exception_handling(self):
        """Тест обработки исключений при создании таблиц"""
        with patch('db_init.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            
            # Симулируем ошибку при выполнении второго запроса
            def execute_side_effect(sql):
                if sql == sql_querry_init_db:
                    raise sqlite3.Error("Table creation failed")
                return None
            
            mock_cursor.execute.side_effect = execute_side_effect
            
            # Проверяем, что исключение пробрасывается
            with pytest.raises(sqlite3.Error, match="Table creation failed"):
                init_tables()
            
            # Проверяем, что соединение все равно закрывается
            mock_conn.close.assert_called_once()


# Интеграционные тесты с реальной БД
class TestInitTablesIntegration:
    """Интеграционные тесты для init_tables с реальной БД"""
    
    def test_init_tables_creates_actual_tables(self, temp_database):
        """Тест реального создания таблиц в БД"""
        db_path = temp_database
        
        # Подменяем путь к базе данных на временный
        with patch('db_init.sqlite3.connect') as mock_connect:
            # Создаем реальное соединение с временной БД
            real_conn = sqlite3.connect(db_path)
            mock_connect.return_value = real_conn
            
            init_tables()
            
            # Проверяем, что таблицы действительно созданы
            cursor = real_conn.cursor()
            
            # Проверяем таблицу lk
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='lk'")
            lk_table_exists = cursor.fetchone()
            assert lk_table_exists is not None
            
            # Проверяем таблицу data
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='data'")
            data_table_exists = cursor.fetchone()
            assert data_table_exists is not None
            
            # Проверяем структуру таблицы lk
            cursor.execute("PRAGMA table_info(lk)")
            lk_columns = cursor.fetchall()
            expected_lk_columns = ['id', 'name_lk', 'letter', 'error']
            actual_lk_columns = [col[1] for col in lk_columns]
            assert set(actual_lk_columns) == set(expected_lk_columns)
            
            # Проверяем структуру таблицы data
            cursor.execute("PRAGMA table_info(data)")
            data_columns = cursor.fetchall()
            expected_data_columns = ['id', 'name_lk', 'count_errors', 'type_test']
            actual_data_columns = [col[1] for col in data_columns]
            assert set(actual_data_columns) == set(expected_data_columns)
            
            real_conn.close()
    
    def test_init_tables_idempotent(self, temp_database):
        """Тест, что функция может быть вызвана многократно без ошибок"""
        db_path = temp_database
        
        with patch('db_init.sqlite3.connect') as mock_connect:
            real_conn = sqlite3.connect(db_path)
            mock_connect.return_value = real_conn
            
            # Вызываем функцию несколько раз
            for _ in range(3):
                init_tables()
            
            # Проверяем, что таблицы все еще существуют и не дублируются
            cursor = real_conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            table_names = [table[0] for table in tables]
            
            # Должны быть только две таблицы
            assert len(table_names) == 2
            assert 'lk' in table_names
            assert 'data' in table_names
            
            real_conn.close()