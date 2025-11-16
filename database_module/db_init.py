sql_querry_init_db = """
    CREATE TABLE IF NOT EXISTS data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name_lk TEXT NOT NULL,
        count_errors INTEGER,
        type_test TEXT 
    )   
"""

sql_querry_init_db_to_grafics = """
    CREATE TABLE IF NOT EXISTS data_to_diograms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name_lk TEXT NOT NULL,
        count_errors INTEGER,
        count_tap_bl INTEGER, 
        count_tap_bl_e INTEGER, 
        count_tap_bp INTEGER, 
        count_tap_bp_e INTEGER, 
        count_tap_ly INTEGER,
        count_tap_ly_e INTEGER,
        count_tap_py INTEGER,
        count_tap_py_e INTEGER,
        count_tap_ls INTEGER,
        count_tap_ls_e INTEGER,
        count_tap_ps INTEGER,
        count_tap_ps_e INTEGER,
        count_tap_lb INTEGER,
        count_tap_lb_e INTEGER,
        count_tap_pb INTEGER,
        count_tap_pb_e INTEGER,
        count_tap_lm INTEGER,
        count_tap_lm_e INTEGER,
        count_tap_pm INTEGER,
        count_tap_pm_e INTEGER
    )   
"""

sql_querry_init_lk = """
    CREATE TABLE IF NOT EXISTS lk (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name_lk TEXT NOT NULL,
        letter TEXT NOT NULL,
        error INTEGER,
        finger TEXT DEFAULT NULL
    ) 
"""

sql_querry_init_finger_stats = """
    CREATE TABLE IF NOT EXISTS finger_statistics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        analysis_id INTEGER NOT NULL,
        finger_code TEXT NOT NULL,
        press_count INTEGER NOT NULL,
        FOREIGN KEY (analysis_id) REFERENCES data (id) ON DELETE CASCADE
    )
"""

import sqlite3

def init_tables():
    """
    Если таблицы не созданы, то он создаст три таблички - одну для хранения результатов рассчетов, 
    вторую для хранения раскладок и третью для статистики по пальцам.
    """

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(f"{sql_querry_init_lk}")
    cursor.execute(f"{sql_querry_init_db}")
    cursor.execute(f"{sql_querry_init_finger_stats}")
    cursor.execute(f"{sql_querry_init_db_to_grafics}")

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


def migrate_database():
    """
    Выполняет миграцию базы данных для поддержки новых функций
    """
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    try:
        # Проверяем, есть ли колонка finger в таблице lk
        cursor.execute("PRAGMA table_info(lk)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'finger' not in columns:
            print("🔄 Добавляем колонку 'finger' в таблицу lk...")
            cursor.execute("ALTER TABLE lk ADD COLUMN finger TEXT DEFAULT NULL")
            print("✅ Колонка 'finger' добавлена")
        
        # Создаем таблицу finger_statistics если её нет
        cursor.execute(sql_querry_init_finger_stats)
        
        conn.commit()
        print("✅ Миграция базы данных завершена")
        
    except Exception as e:
        print(f"❌ Ошибка миграции базы данных: {e}")
        conn.rollback()
    finally:
        conn.close()