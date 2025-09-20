import sqlite3


def take_lk_from_db(name: str) -> dict | None:
    """
    Возвращает словарь правил раскладки, по ее имени
    Если такой раскладки нет - вернет None
    """
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("select letter, error from lk where name_lk = ?", (name,))

    data = cursor.fetchall()

    conn.commit()
    conn.close()
    if len(data) > 10:
        result = {}

        for pair in data:
            result[pair[0]] = pair[1]

        return result
    else:
        return None

def take_all_data_from_lk() -> list:
    """
    Возвращает все содержимое из таблицы lk(с раскладками), включая тестовые
    """
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("select * from lk")

    data = cursor.fetchall()

    conn.commit()
    conn.close()

    return data

def take_lk_names_from_lk() -> list:
    """
    Врозвращает список всех имеющихся в бд раскладок,
    кроме тех, в названии которых есть слово test.
    """
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("select distinct name_lk from lk")

    data = cursor.fetchall()
    filtered_data = list(filter(lambda x: 'test' not in x, data))

    conn.commit()
    conn.close()

    return  filtered_data


def save_analysis_result(layout_name: str, result: dict, file_path: str, analysis_type: str = "words") -> int:
    """
    Сохраняет результаты анализа в таблицу data
    
    Args:
        layout_name: Название раскладки
        result: Результаты анализа
        file_path: Путь к анализируемому файлу
        analysis_type: Тип анализа ('words' или 'text')
    
    Returns:
        int: ID созданной записи
    """
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    # Формируем тип теста с дополнительной информацией
    test_type = f"{analysis_type}|{file_path}|{result['total_words']}w|{result['total_characters']}c"
    
    cursor.execute(
        "INSERT INTO data (name_lk, count_errors, type_test) VALUES (?, ?, ?)",
        (layout_name, result['total_errors'], test_type)
    )
    
    record_id = cursor.lastrowid
    
    conn.commit()
    conn.close()
    
    return record_id


def get_analysis_history(layout_name: str = None, limit: int = 50) -> list:
    """
    Получает историю анализов из базы данных
    
    Args:
        layout_name: Название раскладки (если None, то все раскладки)
        limit: Максимальное количество записей
    
    Returns:
        list: Список записей с результатами
    """
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    if layout_name:
        cursor.execute(
            "SELECT id, name_lk, count_errors, type_test FROM data WHERE name_lk = ? ORDER BY id DESC LIMIT ?",
            (layout_name, limit)
        )
    else:
        cursor.execute(
            "SELECT id, name_lk, count_errors, type_test FROM data ORDER BY id DESC LIMIT ?",
            (limit,)
        )
    
    data = cursor.fetchall()
    
    conn.commit()
    conn.close()
    
    return data


def get_analysis_statistics(layout_name: str) -> dict:
    """
    Получает статистику анализов для раскладки
    
    Args:
        layout_name: Название раскладки
    
    Returns:
        dict: Статистика анализов
    """
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            COUNT(*) as total_tests,
            AVG(count_errors) as avg_errors,
            MIN(count_errors) as min_errors,
            MAX(count_errors) as max_errors
        FROM data 
        WHERE name_lk = ?
    """, (layout_name,))
    
    result = cursor.fetchone()
    
    conn.commit()
    conn.close()
    
    if result and result[0] > 0:
        return {
            'total_tests': result[0],
            'avg_errors': result[1],
            'min_errors': result[2],
            'max_errors': result[3]
        }
    else:
        return {
            'total_tests': 0,
            'avg_errors': 0,
            'min_errors': 0,
            'max_errors': 0
        }


def delete_analysis_result(record_id: int) -> bool:
    """
    Удаляет результат анализа по ID
    
    Args:
        record_id: ID записи для удаления
    
    Returns:
        bool: True если запись была удалена
    """
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM data WHERE id = ?", (record_id,))
    deleted_rows = cursor.rowcount
    
    conn.commit()
    conn.close()
    
    return deleted_rows > 0