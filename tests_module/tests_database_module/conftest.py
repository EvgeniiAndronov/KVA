import pytest
import sqlite3
import tempfile
import os
import sys

# Добавляем путь для импорта модулей
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# SQL-запросы для создания таблиц (из db_init.py)
SQL_QUERY_INIT_DB = """
    CREATE TABLE IF NOT EXISTS data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name_lk TEXT NOT NULL,
        count_errors INTEGER,
        type_test TEXT 
    )   
"""

SQL_QUERY_INIT_LK = """
    CREATE TABLE IF NOT EXISTS lk (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name_lk TEXT NOT NULL,
        letter TEXT NOT NULL,
        error INTEGER
    ) 
"""

@pytest.fixture
def temp_database():
    """Создает временную базу данных для интеграционных тестов"""
    fd, temp_path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    
    yield temp_path
    
    # Удаляем временный файл после теста
    if os.path.exists(temp_path):
        os.unlink(temp_path)

@pytest.fixture
def temp_database_with_tables():
    """Создает временную базу данных с созданными таблицами"""
    fd, temp_path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    
    # Создаем соединение и таблицы
    conn = sqlite3.connect(temp_path)
    cursor = conn.cursor()
    
    cursor.execute(SQL_QUERY_INIT_LK)
    cursor.execute(SQL_QUERY_INIT_DB)
    
    conn.commit()
    conn.close()
    
    yield temp_path
    
    # Удаляем временный файл после теста
    if os.path.exists(temp_path):
        os.unlink(temp_path)

@pytest.fixture
def sample_lk_data(temp_database_with_tables):
    """Фикстура с тестовыми данными в таблице lk"""
    db_path = temp_database_with_tables
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Добавляем тестовые данные в таблицу lk
    test_data = [
        ('layout1', 'a', 1),
        ('layout1', 'b', 2),
        ('layout2', 'a', 5),
        ('test_layout', 'c', 3),
        ('русская', 'а', 10),
    ]
    
    for name, letter, error in test_data:
        cursor.execute(
            "INSERT INTO lk (name_lk, letter, error) VALUES (?, ?, ?)",
            (name, letter, error)
        )
    
    conn.commit()
    conn.close()
    
    return db_path

@pytest.fixture
def sample_analysis_data(temp_database_with_tables):
    """Фикстура с тестовыми данными для анализа"""
    db_path = temp_database_with_tables
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Добавляем тестовые данные в таблицу data
    test_records = [
        ('layout1', 5, 'words|file1.txt|100w|500c'),
        ('layout1', 3, 'text|file2.txt|50w|250c'),
        ('layout2', 7, 'words|file3.txt|150w|750c'),
        ('layout1', 2, 'words|file4.txt|80w|400c'),
        ('layout2', 4, 'text|file5.txt|60w|300c'),
    ]
    
    for record in test_records:
        cursor.execute(
            "INSERT INTO data (name_lk, count_errors, type_test) VALUES (?, ?, ?)",
            record
        )
    
    conn.commit()
    conn.close()
    
    return db_path