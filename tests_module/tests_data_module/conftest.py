# fixtures/test_data_fixtures.py
import pytest
import tempfile
import os


@pytest.fixture
def temp_dir():
    """Фикстура для создания временной директории"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield tmp_dir


@pytest.fixture
def sample_result_basic():
    """Базовая фикстура с результатами анализа"""
    return {
        'total_errors': 100,
        'total_words': 50,
        'total_characters': 200,
        'processed_characters': 180,
        'unknown_characters': {'@', '#'},
        'avg_errors_per_word': 2.0,
        'avg_errors_per_char': 0.01,
        'text_type': 'words'
    }


@pytest.fixture
def sample_result_high_errors():
    """Фикстура с высоким уровнем ошибок"""
    return {
        'total_errors': 1000,
        'total_words': 100,
        'total_characters': 500,
        'processed_characters': 400,
        'unknown_characters': {'@', '#', '$', '%'},
        'avg_errors_per_word': 10.0,
        'avg_errors_per_char': 2.0,
        'text_type': 'words'
    }


@pytest.fixture
def sample_result_no_errors():
    """Фикстура без ошибок"""
    return {
        'total_errors': 0,
        'total_words': 100,
        'total_characters': 500,
        'processed_characters': 500,
        'unknown_characters': set(),
        'avg_errors_per_word': 0.0,
        'avg_errors_per_char': 0.0,
        'text_type': 'words'
    }


@pytest.fixture
def sample_result_minimal():
    """Фикстура с минимальными данными"""
    return {
        'total_errors': 1,
        'total_words': 1,
        'total_characters': 10,
        'processed_characters': 8,
        'unknown_characters': set(),
        'avg_errors_per_word': 1.0,
        'avg_errors_per_char': 0.1,
        'text_type': 'words'
    }


@pytest.fixture
def sample_unknown_chars():
    """Фикстура с неизвестными символами"""
    return {'@', '#', '$', '€', '©'}


@pytest.fixture
def sample_unknown_chars_special():
    """Фикстура со специальными символами"""
    return {'\n', '\t', ' ', '®'}


@pytest.fixture
def sample_results_list():
    """Фикстура со списком результатов для детального отчета"""
    return [
        {
            'result': {
                'total_errors': 100,
                'total_words': 50,
                'total_characters': 200,
                'processed_characters': 180,
                'unknown_characters': {'@'},
                'avg_errors_per_word': 2.0,
                'avg_errors_per_char': 0.01,
                'text_type': 'words'
            },
            'file_path': '/path/to/file1.txt',
            'layout_name': 'layout1',
            'timestamp': '2024-01-01 10:00:00'
        },
        {
            'result': {
                'total_errors': 50,
                'total_words': 60,
                'total_characters': 250,
                'processed_characters': 240,
                'unknown_characters': {'#'},
                'avg_errors_per_word': 0.83,
                'avg_errors_per_char': 0.002,
                'text_type': 'words'
            },
            'file_path': '/path/to/file2.txt',
            'layout_name': 'layout2',
            'timestamp': '2024-01-01 11:00:00'
        }
    ]


@pytest.fixture
def mock_db_connection(mocker):
    """Фикстура для мока соединения с БД"""
    mock_conn = mocker.Mock()
    mock_cursor = mocker.Mock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn, mock_cursor


@pytest.fixture
def layout_comparison_data():
    """Фикстура с данными для сравнения раскладок"""
    return [
        ('layout1', 5, 2.0, 1, 4),
        ('layout2', 3, 3.5, 2, 5),
        ('layout3', 4, 1.5, 1, 3)
    ]


@pytest.fixture
def history_data():
    """Фикстура с историческими данными"""
    return [
        (1, 10, 'words'), (2, 8, 'words'), (3, 5, 'words'),
        (4, 7, 'words'), (5, 3, 'words')
    ]