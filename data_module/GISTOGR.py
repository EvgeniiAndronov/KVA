import matplotlib.pyplot as plt
import numpy as np

# --- КОНСТАНТЫ ЦВЕТОВ ---
COLOR_YTSUKEN_HIST = '#FF0000'  # Красный (теперь будет последним)
COLOR_DIKTOR_HIST = '#F9E969'  # Жёлтый
COLOR_VISOV_HIST = '000000'  # Чёрный
COLOR_ANT_HIST = '#B3DCFD'  # Голубой
COLOR_SCOROPIS_HIST = '#77DD77'  # Зеленый
COLOR_ZUBACHEV_HIST = '#E383EF'  # Фиолетовый
COLOR_RUSFON_HIST = '#FFC0CB'  # Розовый


# --- Функция для рисования ГОРИЗОНТАЛЬНОЙ ГИСТОГРАММЫ для 7 раскладок ---
def plot_finger_usage_7_layouts_only_with_fines(
        layout_ytsuken, fines_ytsuken,
        layout_dictor, fines_dictor,
        layout_visov, fines_visov,
        layout_ant, fines_ant,
        layout_scoropis, fines_scoropis,
        layout_zubachev, fines_zubachev,
        layout_rusfon, fines_rusfon,
        ln
):
    """
    Рисует горизонтальную гистограмму, сравнивая нагрузки на пальцы
    для 7 раскладок, с отображением нагрузки и штрафов.
    'Йцукен' теперь идет последним.
    """
    fingers = ['Л_Большой', 'П_Большой', 'Л_Указательный', 'П_Указательный', 'Л_Средний', 'П_Средний', 'Л_Безымянный',
               'П_Безымянный', 'Л_Мизинец', 'П_Мизинец']

    # Цвета для каждой раскладки. ЙЦУКЕН теперь последний.
    colors = [
        COLOR_DIKTOR_HIST,
        COLOR_VISOV_HIST,
        COLOR_ANT_HIST,
        COLOR_SCOROPIS_HIST,
        COLOR_ZUBACHEV_HIST,
        COLOR_RUSFON_HIST,
        COLOR_YTSUKEN_HIST  # ЙЦУКЕН последний
    ]

    # Объединяем данные нагрузки. ЙЦУКЕН теперь последний.
    all_layouts_load = [
        layout_dictor,
        layout_visov,
        layout_ant,
        layout_scoropis,
        layout_zubachev,
        layout_rusfon,
        layout_ytsuken  # ЙЦУКЕН последний
    ]

    # Объединяем данные штрафов. ЙЦУКЕН теперь последний.
    all_fines_load = [
        fines_dictor,
        fines_visov,
        fines_ant,
        fines_scoropis,
        fines_zubachev,
        fines_rusfon,
        fines_ytsuken  # ЙЦУКЕН последний
    ]

    # Названия раскладок для легенды. ЙЦУКЕН теперь последний.
    # layout_names = ['Диктор', 'Вызов', 'Ант', 'Скоропись', 'Зубачев', 'РусФон', 'Йцукен']
    layout_names = ln

    num_fingers = len(fingers)
    num_layouts = len(all_layouts_load)

    index = np.arange(num_fingers)
    bar_width = 0.12

    total_width = num_layouts * bar_width
    start_pos = -total_width / 2 + bar_width / 2

    fig, ax = plt.subplots(figsize=(14, 10))

    max_total_load = 0

    # Рисуем столбцы для каждой раскладки
    for i in range(num_layouts):
        current_layout = all_layouts_load[i]
        current_fines = all_fines_load[i]
        current_color = colors[i]
        current_name = layout_names[i]

        current_offset = start_pos + i * bar_width

        rects = ax.barh(index + current_offset, current_layout, bar_width,
                        label=current_name, color=current_color, alpha=1.0)

        # --- Добавляем текст нагрузки и штрафов справа от каждого столбика ---
        for rect, fine_value in zip(rects, current_fines):
            width = rect.get_width()
            y_pos = rect.get_y() + rect.get_height() / 2

            text_to_display = f"Н:{width:.0f}; Ш:{fine_value:.0f}"

            ax.text(width, y_pos, f" {text_to_display}",
                    va='center', ha='left', fontsize=5, color='black')

        current_max_load = max(current_layout)
        if current_max_load > max_total_load:
            max_total_load = current_max_load

    ax.set_ylabel('Пальцы')
    ax.set_xlabel('Количество нажатий + количество штрафов')
    ax.set_title('Сравнение нагрузок и штрафов на пальцы по раскладкам', fontsize=14, fontweight='bold')

    ax.set_yticks(index, fingers)

    ax.set_xlim(0, max_total_load * 1.25)

    ax.legend(loc='upper right')

    plt.tight_layout()
    plt.show()


# --- Входные данные ---

# Данные для гистограммы (7 раскладок)
layout_dictor = [308809, 252662, 622693, 1208801, 247804, 574163, 225677, 506704, 205019, 407680]  # Диктор
layout_visov = [280736, 280736, 654094, 693976, 908794, 384139, 195100, 148917, 264718, 354770]  # Вызов
layout_ant = [150000, 180000, 500000, 400000, 200000, 90000, 70000, 30000, 100000, 80000]
layout_scoropis = [80000, 100000, 600000, 550000, 150000, 50000, 40000, 20000, 70000, 60000]
layout_zubachev = [400000, 120000, 700000, 600000, 300000, 150000, 100000, 40000, 150000, 100000]
layout_rusfon = [200000, 220000, 550000, 450000, 220000, 100000, 80000, 35000, 90000, 70000]
layout_ytsuken = [336883, 224588, 1819640, 1300013, 685725, 231567, 161738, 73896, 401456,
                  293521]  # Йцукен (теперь последний)

# --- Примерные данные штрафов ---
fines_dictor = [80, 60, 120, 100, 30, 40, 20, 30, 15, 25]
fines_visov = [90, 90, 130, 110, 80, 35, 18, 15, 25, 35]
fines_ant = [40, 50, 100, 90, 30, 15, 10, 5, 20, 15]
fines_scoropis = [20, 30, 120, 110, 40, 25, 20, 10, 15, 12]
fines_zubachev = [150, 40, 180, 170, 100, 50, 30, 15, 45, 35]
fines_rusfon = [70, 80, 110, 100, 50, 25, 18, 8, 22, 18]
fines_ytsuken = [100, 50, 150, 120, 60, 20, 15, 5, 40, 30]  # Йцукен (теперь последний)

# --- Вызов функции для построения только гистограммы с штрафами ---
# plot_finger_usage_7_layouts_only_with_fines(
#     layout_ytsuken, fines_ytsuken,
#     layout_dictor, fines_dictor,
#     layout_visov, fines_visov,
#     layout_ant, fines_ant,
#     layout_scoropis, fines_scoropis,
#     layout_zubachev, fines_zubachev,
#     layout_rusfon, fines_rusfon
# )