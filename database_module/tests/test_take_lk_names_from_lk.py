import pytest
from unittest.mock import Mock, patch
from database import take_lk_names_from_lk


class TestTakeLkNamesFromLk:
    """Тесты для функции take_lk_names_from_lk"""
    
    def test_take_lk_names_success(self):
        """Тест успешного получения имен раскладок"""
        # Мокируем тестовые данные
        test_data = [
            ('layout1',),
            ('layout2',),
            ('test_layout',),  # Должен быть отфильтрован
            ('layout3',),
            ('another_test',)  # Должен быть отфильтрован
        ]
        
        with patch('database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchall.return_value = test_data
            
            result = take_lk_names_from_lk()
            
            # Проверяем правильность вызовов
            mock_connect.assert_called_once_with("database.db")
            mock_cursor.execute.assert_called_once_with("select distinct name_lk from lk")
            mock_conn.commit.assert_called_once()
            mock_conn.close.assert_called_once()
            
            # Проверяем результат (фильтрация test-раскладок)
            expected_result = [('layout1',), ('layout2',), ('layout3',)]
            assert result == expected_result
    
    def test_take_lk_names_only_test_layouts(self):
        """Тест, когда есть только тестовые раскладки"""
        test_data = [
            ('test_layout1',),
            ('test_layout2',),
            ('another_test',)
        ]
        
        with patch('database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchall.return_value = test_data
            
            result = take_lk_names_from_lk()
            
            # Все раскладки должны быть отфильтрованы
            assert result == []
    
    def test_take_lk_names_empty(self):
        """Тест получения имен из пустой таблицы"""
        with patch('database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchall.return_value = []  # Пустая таблица
            
            result = take_lk_names_from_lk()
            
            assert result == []
    
    @pytest.mark.parametrize("test_data,expected", [
        ([('layout1',), ('test_layout',)], [('layout1',)]),
        ([('normal',), ('test',), ('TEST_UPPER',)], [('normal',)]),
        ([], []),
        ([('test1',), ('test2',)], []),
    ])
    def test_various_filtering_scenarios(self, test_data, expected):
        """Параметризованный тест различных сценариев фильтрации"""
        with patch('database.sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.fetchall.return_value = test_data
            
            result = take_lk_names_from_lk()
            
            assert result == expected