import sqlite3

sql_querry_take_lk = """
    select letter, error from lk where name_lk = ?
"""


def take_lk_from_db(name: str) -> dict:
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(f"{sql_querry_take_lk}", (name,))

    data = cursor.fetchall()

    conn.commit()
    conn.close()

    result = {}

    for pair in data:
        result[pair[0]] = pair[1]

    return result

def take_all_data_from_lk():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("select * from lk")

    data = cursor.fetchall()

    conn.commit()
    conn.close()

