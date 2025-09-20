sql_querry_init_db = """
    CREATE TABLE IF NOT EXISTS data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name_lk TEXT NOT NULL,
        count_errors INTEGER,
        type_test TEXT 
    )   
"""

sql_querry_init_lk = """
    CREATE TABLE IF NOT EXISTS lk (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name_lk TEXT NOT NULL,
        letter TEXT NOT NULL,
        error INTEGER
    ) 
"""

import sqlite3

def init_tables():
    """
    Если таблицы не созданы, то он создаст две таблички - одну для хранения результатов рассчетов, а вторую для хранения раскладок.
    """

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(f"{sql_querry_init_lk}")
    cursor.execute(f"{sql_querry_init_db}")

    conn.commit()
    conn.close()

def make_mok_data(start_letter: str, name_test_lk: str):
    """
    Добавление тестовых данных в бд, для проведения тестирования методов на базе данных.
    """
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    for i in range(26):
        cursor.execute("insert into lk (name_lk, letter, error) VALUES (?, ?, ?)",
                       (f"{name_test_lk}", f"{chr(ord(f"{start_letter}") + i)}", i))

    for i in range(10):
        cursor.execute("insert into lk (name_lk, letter, error) VALUES (?, ?, ?)",
                       (f"{name_test_lk}", f"{chr(ord(f"1") + i)}", i))

    conn.commit()
    conn.close()

    print("add test data in database")