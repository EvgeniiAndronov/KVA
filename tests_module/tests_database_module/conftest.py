import sys
import os
import pytest
import sqlite3
from unittest.mock import Mock, MagicMock

# Добавляем путь к корневой директории проекта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Фикстуры для тестов базы данных
@pytest.fixture
def mock_db_connection():
    """
    Фикстура для мок-подключения к базе данных
    Возвращает кортеж: (mock_connect, mock_conn, mock_cursor)
    """
    with pytest.MonkeyPatch().context() as m:
        mock_connect = Mock()
        mock_conn = Mock()
        mock_cursor = Mock()
        
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Патчим sqlite3.connect во всех модулях
        m.setattr('database_module.database.sqlite3.connect', mock_connect)
        m.setattr('database_module.db_init.sqlite3.connect', mock_connect)
        
        yield mock_connect, mock_conn, mock_cursor

@pytest.fixture
def sample_layout_data():
    """
    Фикстура с тестовыми данными раскладки клавиатуры
    """
    return [
        ('a', 1), ('b', 2), ('c', 3), ('d', 4), ('e', 5),
        ('f', 6), ('g', 7), ('h', 8), ('i', 9), ('j', 10),
        ('k', 11), ('l', 12), ('m', 13), ('n', 14), ('o', 15),
        ('p', 16), ('q', 17), ('r', 18), ('s', 19), ('t', 20),
        ('u', 21), ('v', 22), ('w', 23), ('x', 24), ('y', 25), ('z', 26)
    ]

@pytest.fixture
def sample_analysis_result():
    """
    Фикстура с тестовыми результатами анализа
    """
    return {
        'total_errors': 5,
        'total_words': 100,
        'total_characters': 500,
        'processed_characters': 500,
        'unknown_characters': set(),
        'text_type': 'words',
        'avg_errors_per_word': 0.05,
        'avg_errors_per_char': 0.01
    }

@pytest.fixture
def sample_layout_dict():
    """
    Фикстура с тестовой раскладкой в виде словаря
    """
    return {
        'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5,
        'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 10,
        'k': 11, 'l': 12, 'm': 13, 'n': 14, 'o': 15
    }

@pytest.fixture
def mock_tqdm():
    """
    Фикстура для мок-объекта tqdm (прогресс-бар)
    """
    with pytest.MonkeyPatch().context() as m:
        mock_tqdm = MagicMock()
        mock_pbar = MagicMock()
        mock_tqdm.return_value = mock_pbar
        
        m.setattr('calculate_data.tqdm', mock_tqdm)
        
        yield mock_tqdm, mock_pbar

@pytest.fixture
def temp_test_file(tmp_path):
    """
    Фикстура для создания временного тестового файла
    """
    def _create_temp_file(content, extension=".txt"):
        temp_file = tmp_path / f"test_file{extension}"
        temp_file.write_text(content, encoding='utf-8')
        return str(temp_file)
    
    return _create_temp_file

@pytest.fixture(scope="session")
def database_url():
    """
    Фикстура с URL тестовой базы данных (сессионная область)
    """
    return "file::memory:?cache=shared"

@pytest.fixture
def sample_analysis_history():
    """
    Фикстура с тестовой историей анализа
    """
    return [
        (1, 'layout1', 5, 'words|file1.txt|100w|500c'),
        (2, 'layout2', 3, 'text|file2.txt|50w|250c'),
        (3, 'layout1', 7, 'words|file3.txt|150w|750c')
    ]

@pytest.fixture
def expected_statistics():
    """
    Фикстура с ожидаемой статистикой анализа
    """
    return {
        'total_tests': 5,
        'avg_errors': 3.5,
        'min_errors': 1,
        'max_errors': 7
    }

# Автоматически используемая фикстура для всех тестов
@pytest.fixture(autouse=True)
def setup_test_environment():
    """
    Автоматически выполняемая фикстура для настройки тестового окружения
    """
    # Сохраняем оригинальные sys.path
    original_path = sys.path.copy()
    
    yield
    
    # Восстанавливаем sys.path после теста
    sys.path = original_path

# Фикстура с параметрами для параметризованных тестов
@pytest.fixture(params=[
    (1, 1, True),    # Существующая запись
    (2, 0, False),   # Несуществующая запись  
    (100, 1, True),  # Другая существующая запись
    (-1, 0, False),  # Отрицательный ID
])
def delete_scenario(request):
    """
    Фикстура с параметрами для тестов удаления записей
    """
    return request.param