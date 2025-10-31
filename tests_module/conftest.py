import pytest
import tempfile
import os
import sys

# Пути к модулям
current_dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(current_dir, '../scan_module'))
sys.path.insert(0, os.path.join(current_dir, '../processing_module'))
sys.path.insert(0, os.path.join(current_dir, '../database_module'))

@pytest.fixture
def temp_file():
    """Временный файл с текстом"""
    fd, temp_path = tempfile.mkstemp(suffix='.txt')
    with os.fdopen(fd, 'w') as f:
        f.write("hello\nworld\ntest\nfile\ncontent\n")
    yield temp_path
    if os.path.exists(temp_path):
        os.unlink(temp_path)

@pytest.fixture
def sample_word_list():
    """Простой список слов"""
    return ["hello", "world", "test"]

@pytest.fixture
def sample_rules_old():
    """Простые правила (старый формат)"""
    return {"a": 1, "b": 2, "c": 3, "h": 1, "e": 2, "l": 1, "o": 3, "w": 2, "r": 1, "d": 1}

@pytest.fixture
def sample_text():
    """Простой текст"""
    return "hello world test"

@pytest.fixture
def temp_db():
    """Временная база данных с тестовыми данными"""
    import database
    original_db = getattr(database, 'DB_PATH', 'database.db')
    
    fd, temp_path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    
    database.DB_PATH = temp_path
    
    from db_init import init_tables
    init_tables()
    
    # Добавляем простую тестовую раскладку
    test_layout = {"a": 1, "b": 2, "c": 3}
    database.save_layout_to_db("test_layout", test_layout)
    
    yield temp_path
    
    database.DB_PATH = original_db
    if os.path.exists(temp_path):
        os.unlink(temp_path)