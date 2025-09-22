import pytest
from unittest.mock import Mock, patch, call
import sys
import os

# Добавляем путь для импорта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from db_init import make_mok_data
import sqlite3


class TestMakeMokData:
    """Тесты для функции make_mok_data"""
    
    def test_make_mok_data_inserts_correct_number_of_records(self):
        """Тест количества вставляемых записей"""
        with patch('db_init.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            
            make_mok_data('a', 'test_layout')
            
            # Проверяем, что было 36 вызовов execute (26 букв + 10 цифр)
            assert mock_cursor.execute.call_count == 36
            
            # Проверяем commit и close
            mock_conn.commit.assert_called_once()
            mock_conn.close.assert_called_once()
    
    def test_make_mok_data_letter_insertions(self):
        """Тест вставки буквенных данных"""
        with patch('db_init.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            
            make_mok_data('a', 'test_layout')
            
            # Проверяем первые 26 вызовов (буквы)
            letter_calls = mock_cursor.execute.call_args_list[:26]
            
            for i, call_args in enumerate(letter_calls):
                expected_letter = chr(ord('a') + i)
                expected_sql = "insert into lk (name_lk, letter, error) VALUES (?, ?, ?)"
                expected_params = ('test_layout', expected_letter, i)
                
                assert call_args[0][0] == expected_sql
                assert call_args[0][1] == expected_params
    
    def test_make_mok_data_digit_insertions(self):
        """Тест вставки цифровых данных"""
        with patch('db_init.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            
            make_mok_data('a', 'test_layout')
            
            # Проверяем последние 10 вызовов (цифры)
            digit_calls = mock_cursor.execute.call_args_list[26:]
            
            for i, call_args in enumerate(digit_calls):
                expected_digit = chr(ord('1') + i)
                expected_sql = "insert into lk (name_lk, letter, error) VALUES (?, ?, ?)"
                expected_params = ('test_layout', expected_digit, i)
                
                assert call_args[0][0] == expected_sql
                assert call_args[0][1] == expected_params
    
    def test_make_mok_data_different_start_letter(self):
        """Тест с различными начальными буквами"""
        test_cases = [
            ('a', 'z'),  # стандартный случай
            ('A', 'Z'),  # заглавные буквы
            ('а', 'я'),  # кириллица
        ]
        
        for start_letter, expected_last_letter in test_cases:
            with patch('db_init.sqlite3.connect') as mock_connect:
                mock_conn = Mock()
                mock_cursor = Mock()
                mock_connect.return_value = mock_conn
                mock_conn.cursor.return_value = mock_cursor
                
                make_mok_data(start_letter, 'test_layout')
                
                # Проверяем первую и последнюю букву
                first_call = mock_cursor.execute.call_args_list[0]
                last_call = mock_cursor.execute.call_args_list[25]  # 26-я буква
                
                assert first_call[0][1] == ('test_layout', start_letter, 0)
                assert last_call[0][1] == ('test_layout', expected_last_letter, 25)
    
    def test_make_mok_data_different_layout_names(self):
        """Тест с различными именами раскладок"""
        test_names = ['test_layout', 'русская_раскладка', 'layout with spaces']
        
        for layout_name in test_names:
            with patch('db_init.sqlite3.connect') as mock_connect:
                mock_conn = Mock()
                mock_cursor = Mock()
                mock_connect.return_value = mock_conn
                mock_conn.cursor.return_value = mock_cursor
                
                make_mok_data('a', layout_name)
                
                # Проверяем, что имя раскладки правильно передается
                first_call = mock_cursor.execute.call_args_list[0]
                assert first_call[0][1][0] == layout_name
    
    def test_make_mok_data_exception_handling(self):
        """Тест обработки исключений при вставке данных"""
        with patch('db_init.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            
            # Симулируем ошибку при вставке
            mock_cursor.execute.side_effect = sqlite3.Error("Insert failed")
            
            # Проверяем, что исключение пробрасывается
            with pytest.raises(sqlite3.Error, match="Insert failed"):
                make_mok_data('a', 'test_layout')
            
            # Проверяем, что соединение все равно закрывается
            mock_conn.close.assert_called_once()


# Интеграционные тесты с реальной БД
class TestMakeMokDataIntegration:
    """Интеграционные тесты для make_mok_data с реальной БД"""
    
    def test_make_mok_data_creates_actual_records(self, temp_database_with_tables):
        """Тест реального создания записей в БД"""
        db_path = temp_database_with_tables
        
        with patch('db_init.sqlite3.connect') as mock_connect:
            real_conn = sqlite3.connect(db_path)
            mock_connect.return_value = real_conn
            
            make_mok_data('a', 'test_layout')
            
            # Проверяем, что данные действительно вставлены
            cursor = real_conn.cursor()
            
            # Проверяем общее количество записей
            cursor.execute("SELECT COUNT(*) FROM lk WHERE name_lk = 'test_layout'")
            count = cursor.fetchone()[0]
            assert count == 36  # 26 букв + 10 цифр
            
            # Проверяем буквы
            cursor.execute("SELECT letter, error FROM lk WHERE name_lk = 'test_layout' AND letter BETWEEN 'a' AND 'z' ORDER BY error")
            letters_data = cursor.fetchall()
            assert len(letters_data) == 26
            
            for i, (letter, error) in enumerate(letters_data):
                expected_letter = chr(ord('a') + i)
                assert letter == expected_letter
                assert error == i
            
            # Проверяем цифры
            cursor.execute("SELECT letter, error FROM lk WHERE name_lk = 'test_layout' AND letter BETWEEN '1' AND ':' ORDER BY error")
            digits_data = cursor.fetchall()
            assert len(digits_data) == 10
            
            for i, (digit, error) in enumerate(digits_data):
                expected_digit = chr(ord('1') + i)
                assert digit == expected_digit
                assert error == i
            
            real_conn.close()
    
    def test_make_mok_data_multiple_calls(self, temp_database_with_tables):
        """Тест многократного вызова функции"""
        db_path = temp_database_with_tables
        
        with patch('db_init.sqlite3.connect') as mock_connect:
            real_conn = sqlite3.connect(db_path)
            mock_connect.return_value = real_conn
            
            # Вызываем функцию дважды с разными именами раскладок
            make_mok_data('a', 'layout1')
            make_mok_data('A', 'layout2')
            
            # Проверяем, что все данные вставлены
            cursor = real_conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM lk WHERE name_lk = 'layout1'")
            count1 = cursor.fetchone()[0]
            assert count1 == 36
            
            cursor.execute("SELECT COUNT(*) FROM lk WHERE name_lk = 'layout2'")
            count2 = cursor.fetchone()[0]
            assert count2 == 36
            
            cursor.execute("SELECT COUNT(DISTINCT name_lk) FROM lk")
            distinct_layouts = cursor.fetchone()[0]
            assert distinct_layouts == 2
            
            real_conn.close()