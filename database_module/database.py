import sqlite3


def take_lk_from_db(name: str) -> dict | None:
    """
    Возвращает словарь правил раскладки, по ее имени
    Если такой раскладки нет - вернет None
    
    Поддерживает как старый формат (только штрафы), так и новый ([штраф, палец])
    """
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("select letter, error, finger from lk where name_lk = ?", (name,))

    data = cursor.fetchall()

    conn.commit()
    conn.close()
    
    if len(data) > 0:
        result = {}

        for row in data:
            letter, error, finger = row
            
            # Если есть информация о пальце, используем новый формат
            if finger is not None and finger.strip():
                result[letter] = [error, finger]
            else:
                # Иначе используем старый формат
                result[letter] = error

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
    Сохраняет результаты анализа в таблицу data и статистику пальцев в finger_statistics
    
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
    
    try:
        # Формируем тип теста с дополнительной информацией
        test_type = f"{analysis_type}|{file_path}|{result['total_words']}w|{result['total_characters']}c"
        
        # Сохраняем основные результаты анализа
        cursor.execute(
            "INSERT INTO data (name_lk, count_errors, type_test) VALUES (?, ?, ?)",
            (layout_name, result['total_errors'], test_type)
        )
        
        record_id = cursor.lastrowid
        
        # Сохраняем статистику по пальцам, если она есть
        if 'finger_statistics' in result and result['finger_statistics']:
            for finger_code, press_count in result['finger_statistics'].items():
                cursor.execute(
                    "INSERT INTO finger_statistics (analysis_id, finger_code, press_count) VALUES (?, ?, ?)",
                    (record_id, finger_code, press_count)
                )
        
        conn.commit()
        return record_id
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


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


def get_finger_statistics(analysis_id: int) -> dict:
    """
    Получает статистику по пальцам для конкретного анализа
    
    Args:
        analysis_id: ID анализа
    
    Returns:
        dict: Словарь со статистикой пальцев {finger_code: press_count}
    """
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT finger_code, press_count FROM finger_statistics WHERE analysis_id = ?",
        (analysis_id,)
    )
    
    data = cursor.fetchall()
    conn.close()
    
    return {finger_code: press_count for finger_code, press_count in data}


def get_aggregated_finger_statistics(layout_name: str = None, limit: int = None) -> dict:
    """
    Получает агрегированную статистику по пальцам
    
    Args:
        layout_name: Название раскладки (если None, то все раскладки)
        limit: Ограничение на количество последних анализов
    
    Returns:
        dict: Агрегированная статистика {finger_code: total_presses}
    """
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    if layout_name:
        if limit:
            # Получаем ID последних анализов для данной раскладки
            cursor.execute(
                """SELECT id FROM data WHERE name_lk = ? 
                   ORDER BY id DESC LIMIT ?""",
                (layout_name, limit)
            )
            analysis_ids = [row[0] for row in cursor.fetchall()]
            
            if not analysis_ids:
                conn.close()
                return {}
            
            # Получаем статистику для этих анализов
            placeholders = ','.join('?' * len(analysis_ids))
            cursor.execute(
                f"""SELECT finger_code, SUM(press_count) as total_presses 
                    FROM finger_statistics 
                    WHERE analysis_id IN ({placeholders})
                    GROUP BY finger_code""",
                analysis_ids
            )
        else:
            # Получаем всю статистику для раскладки
            cursor.execute(
                """SELECT fs.finger_code, SUM(fs.press_count) as total_presses 
                   FROM finger_statistics fs
                   JOIN data d ON fs.analysis_id = d.id
                   WHERE d.name_lk = ?
                   GROUP BY fs.finger_code""",
                (layout_name,)
            )
    else:
        if limit:
            # Получаем ID последних анализов
            cursor.execute("SELECT id FROM data ORDER BY id DESC LIMIT ?", (limit,))
            analysis_ids = [row[0] for row in cursor.fetchall()]
            
            if not analysis_ids:
                conn.close()
                return {}
            
            placeholders = ','.join('?' * len(analysis_ids))
            cursor.execute(
                f"""SELECT finger_code, SUM(press_count) as total_presses 
                    FROM finger_statistics 
                    WHERE analysis_id IN ({placeholders})
                    GROUP BY finger_code""",
                analysis_ids
            )
        else:
            # Получаем всю статистику
            cursor.execute(
                """SELECT finger_code, SUM(press_count) as total_presses 
                   FROM finger_statistics 
                   GROUP BY finger_code"""
            )
    
    data = cursor.fetchall()
    conn.close()
    
    return {finger_code: total_presses for finger_code, total_presses in data}


def get_finger_statistics_comparison(layout_names: list) -> dict:
    """
    Сравнивает статистику пальцев между несколькими раскладками
    
    Args:
        layout_names: Список названий раскладок для сравнения
    
    Returns:
        dict: Словарь вида {layout_name: {finger_code: total_presses}}
    """
    result = {}
    
    for layout_name in layout_names:
        result[layout_name] = get_aggregated_finger_statistics(layout_name)
    
    return result


def delete_finger_statistics(analysis_id: int) -> bool:
    """
    Удаляет статистику пальцев для конкретного анализа
    
    Args:
        analysis_id: ID анализа
    
    Returns:
        bool: True если данные были удалены
    """
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM finger_statistics WHERE analysis_id = ?", (analysis_id,))
    deleted_rows = cursor.rowcount
    
    conn.commit()
    conn.close()
    
    return deleted_rows > 0


def save_layout_to_db(layout_name: str, layout: dict) -> bool:
    """
    Сохраняет раскладку в базу данных
    Поддерживает как старый формат (число), так и новый ([штраф, палец])
    
    Args:
        layout_name: Название раскладки
        layout: Словарь раскладки
    
    Returns:
        bool: True если сохранение прошло успешно
    """
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    try:
        # Удаляем старую раскладку с таким же именем
        cursor.execute("DELETE FROM lk WHERE name_lk = ?", (layout_name,))
        
        # Добавляем новую раскладку
        for symbol, rule_data in layout.items():
            if isinstance(rule_data, (int, float)):
                # Старый формат: только штраф
                cursor.execute(
                    "INSERT INTO lk (name_lk, letter, error, finger) VALUES (?, ?, ?, ?)",
                    (layout_name, symbol, rule_data, None)
                )
            elif isinstance(rule_data, list) and len(rule_data) >= 2:
                # Новый формат: [штраф, палец]
                penalty, finger = rule_data[0], rule_data[1]
                cursor.execute(
                    "INSERT INTO lk (name_lk, letter, error, finger) VALUES (?, ?, ?, ?)",
                    (layout_name, symbol, penalty, finger)
                )
            else:
                # Неверный формат, пропускаем
                continue
        
        conn.commit()
        return True
        
    except Exception as e:
        print(f"❌ Ошибка сохранения раскладки в БД: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()