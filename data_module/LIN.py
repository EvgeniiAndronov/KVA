import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# --- КОНСТАНТЫ ЦВЕТОВ ДЛЯ ЛИНИЙ ---
# Цвета для 7 раскладок
COLORS_LINES = [
    '#FF0000',  # Йцукен (Красный)
    '#F9E969',  # Диктор (Жёлтый)
    '#000000',  # Вызов (Чёрный)
    '#B3DCFD',  # Ант (Голубой)
    '#77DD77',  # Скоропись (Зеленый)
    '#E383EF',  # Зубачев (Фиолетовый)
    '#FFC0CB'  # РусФон (Розовый)
]

# Названия раскладок для легенды
LAYOUT_NAMES_LINES = ['Йцукен', 'Диктор', 'Вызов', 'Ант', 'Скоропись', 'Зубачев', 'РусФон']


# --- Вспомогательная функция для подготовки данных ---
def prepare_data(data, layout_name, finger_types):
    """
    Преобразует сырые данные {'left': [...], 'right': [...]}
    в DataFrame для конкретной раскладки.
    """
    all_finger_names = []
    loads = []
    layout_names_series = []  # Серия для имени раскладки

    # Проверяем, что данные 'left' и 'right' имеют одинаковую длину
    if len(data.get('left', [])) != len(finger_types) or len(data.get('right', [])) != len(finger_types):
        print(
            f"Внимание: Количество элементов в 'left' или 'right' для раскладки '{layout_name}' не совпадает с количеством типов пальцев ({len(finger_types)}).")

        # Если данных не хватает, дополним нулями до нужной длины finger_types
        left_loads = data.get('left', []) + [0] * (len(finger_types) - len(data.get('left', [])))
        right_loads = data.get('right', []) + [0] * (len(finger_types) - len(data.get('right', [])))
    else:
        left_loads = data.get('left', [])
        right_loads = data.get('right', [])

    for i in range(len(finger_types)):  # Итерируемся по типам пальцев
        # Проверяем, что индексы существуют
        if i < len(left_loads):
            left_load = left_loads[i]
        else:
            left_load = 0
        if i < len(right_loads):
            right_load = right_loads[i]
        else:
            right_load = 0

        all_finger_names.append(f"{finger_types[i]} Л")
        loads.append(left_load)
        layout_names_series.append(layout_name)

        all_finger_names.append(f"{finger_types[i]} П")
        loads.append(right_load)
        layout_names_series.append(layout_name)

    return pd.DataFrame({
        'Палец': all_finger_names,
        'Нагрузка': loads,
        'Раскладка': layout_names_series
    })


# --- Основная функция для построения 5 линейных графиков ---
def plot_finger_loads_by_layout_7_layouts(data_dictor, data_ytsuken, data_visov,
                                          data_ant, data_scoropis, data_zubachev, data_rusfon):
    """
    Рисует 5 линейных графиков (по одному на тип пальца),
    сравнивая нагрузки для 7 раскладок. Легенда вынесена за пределы графика.
    """
    finger_types = ['Большой', 'Указательный', 'Средний', 'Безымянный', 'Мизинец']

    all_data_frames = []

    all_data_frames.append(prepare_data(data_ytsuken, 'Йцукен', finger_types))
    all_data_frames.append(prepare_data(data_dictor, 'Диктор', finger_types))
    all_data_frames.append(prepare_data(data_visov, 'Вызов', finger_types))
    all_data_frames.append(prepare_data(data_ant, 'Ант', finger_types))
    all_data_frames.append(prepare_data(data_scoropis, 'Скоропись', finger_types))
    all_data_frames.append(prepare_data(data_zubachev, 'Зубачев', finger_types))
    all_data_frames.append(prepare_data(data_rusfon, 'РусФон', finger_types))

    df_all = pd.concat(all_data_frames, ignore_index=True)

    n_rows = 3
    n_cols = 2
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(16, 15))
    axes = axes.flatten()

    # --- Рисуем графики для каждого типа пальца ---
    for i, finger_type in enumerate(finger_types):
        ax = axes[i]

        df_current_finger_type = df_all[df_all['Палец'].str.startswith(finger_type)]

        # Рисуем линии для каждой раскладки
        for j, layout_name in enumerate(LAYOUT_NAMES_LINES):
            df_layout_finger = df_current_finger_type[df_current_finger_type['Раскладка'] == layout_name].sort_values(
                by='Палец')
            df_layout_finger = df_layout_finger.sort_values(by='Палец', key=lambda x: x.str.split('_').str[-1].map(
                {'Л': 0, 'П': 1}))

            ax.plot(df_layout_finger['Палец'], df_layout_finger['Нагрузка'], marker='o', linestyle='-',
                    label=layout_name, color=COLORS_LINES[j])

        ax.set_title(f'Нагрузка на "{finger_type}" пальцы', fontsize=8, fontweight='bold')
        ax.set_ylabel('Кол-во нажатий')
        ax.ticklabel_format(style='plain', axis='y')

        if not df_layout_finger.empty:
            ax.set_xticklabels(df_layout_finger['Палец'], rotation=10, ha='right', fontsize=5)

        # Выносим легенду за пределы графика, справа
        # bbox_to_anchor=(1.05, 1) - означает: 1.05 ширины графика от левого края (т.е. справа от графика), 1 высота графика (верх).
        # loc='upper left' - точка на легенде, которую мы привязываем к bbox_to_anchor.
        # borderaxespad=0. - расстояние между графиком и легендой.
        ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0.)

    # --- Удаляем лишние пустые оси ---
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.suptitle("Сравнение нагрузок на пальцы по раскладкам", fontsize=18, fontweight='bold')

    # rect=[left, bottom, right, top] - это коррекция для suptitle и вынесенных легенд
    plt.tight_layout(rect=[0, 0.03, 0.85, 0.95])

    plt.show()


# --- Пример входных данных ---
data_dictor = {
    'left': [308809, 622693, 247804, 225677, 205019],
    'right': [252662, 1208801, 574163, 506704, 407680]
}
data_ytsuken = {
    'left': [336883, 1819640, 685725, 161738, 401456],
    'right': [224588, 1300013, 231567, 73896, 293521]
}
data_visov = {
    'left': [280736, 654094, 908794, 195100, 264718],
    'right': [280736, 693976, 384139, 148917, 354770]
}

data_ant = {
    'left': [150000, 500000, 200000, 70000, 100000],
    'right': [180000, 400000, 90000, 30000, 80000]
}
data_scoropis = {
    'left': [80000, 600000, 150000, 40000, 70000],
    'right': [100000, 550000, 50000, 20000, 60000]
}
data_zubachev = {
    'left': [400000, 700000, 300000, 100000, 150000],
    'right': [120000, 600000, 150000, 40000, 100000]
}
data_rusfon = {
    'left': [200000, 550000, 220000, 80000, 90000],
    'right': [220000, 450000, 100000, 35000, 70000]
}

# --- Вызов основной функции ---
plot_finger_loads_by_layout_7_layouts(
    data_dictor, data_ytsuken, data_visov,
    data_ant, data_scoropis, data_zubachev, data_rusfon
)