import sqlite3
from GISTOGR import plot_finger_usage_7_layouts_only_with_fines


def get_data_for_diagrams() -> list:
    """
    Получает все данные из таблицы data_to_diograms для построения диаграмм.
    """
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM data_to_diograms")
    data = cursor.fetchall()
    
    conn.close()
    
    return data


def process_data_for_plotting():
    """
    Обрабатывает данные из базы и строит диаграммы.
    """
    data = get_data_for_diagrams()
    
    if not data:
        print("Нет данных для построения диаграмм")
        return
    
    # Группируем данные по названию раскладки
    result = {}
    for row in data:
        layout_name = row[1]  # name_lk
        if layout_name not in result:
            # Инициализируем список нулями для всех полей (22 поля кроме id и name_lk)
            result[layout_name] = [0] * 21
    
    # Суммируем данные для каждой раскладки
    for row in data:
        layout_name = row[1]
        for i in range(2, len(row)):  # Пропускаем id и name_lk
            result[layout_name][i-2] += row[i] if row[i] is not None else 0
    
    # Подготавливаем данные для построения графиков
    layout_names = []
    fingers_tap_data = []
    errors_finger_data = []
    
    for layout_name, values in result.items():
        layout_names.append(layout_name)
        
        # Данные по нажатиям (четные индексы)
        taps = [
            values[1],   # count_tap_bl
            values[3],   # count_tap_bp  
            values[5],   # count_tap_ly
            values[7],   # count_tap_py
            values[9],   # count_tap_ls
            values[11],  # count_tap_ps
            values[13],  # count_tap_lb
            values[15],  # count_tap_pb
            values[17],  # count_tap_lm
            values[19]   # count_tap_pm
        ]
        
        # Данные по ошибкам (нечетные индексы)
        errors = [
            values[2],   # count_tap_bl_e
            values[4],   # count_tap_bp_e
            values[6],   # count_tap_ly_e
            values[8],   # count_tap_py_e
            values[10],  # count_tap_ls_e
            values[12],  # count_tap_ps_e
            values[14],  # count_tap_lb_e
            values[16],  # count_tap_pb_e
            values[18],  # count_tap_lm_e
            values[20]   # count_tap_pm_e
        ]
        
        fingers_tap_data.append(taps)
        errors_finger_data.append(errors)
    
    print(f"Раскладки: {layout_names}")
    print(f"Данные по нажатиям: {fingers_tap_data}")
    print(f"Данные по ошибкам: {errors_finger_data}")
    
    # Строим диаграммы (максимум 7 раскладок)
    max_layouts = min(7, len(layout_names))
    
    if max_layouts >= 1:
        plot_finger_usage_7_layouts_only_with_fines(
            *[item for layout in zip(fingers_tap_data[:max_layouts], errors_finger_data[:max_layouts]) for item in layout], layout_names
        )
    else:
        print("Недостаточно данных для построения диаграмм")


def clear_database():
    """
    Очищает таблицу data_to_diograms.
    """
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM data_to_diograms")
    conn.commit()
    conn.close()
    
    print("База данных очищена")


if __name__ == "__main__":
    process_data_for_plotting()