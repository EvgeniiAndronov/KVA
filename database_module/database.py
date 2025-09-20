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