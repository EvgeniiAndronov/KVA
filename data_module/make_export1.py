import matplotlib.pyplot as plt
import numpy as np

# --- КОНСТАНТЫ ЦВЕТОВ ---
COLOR_LEFT = '#B3DCFD'  # голубой
COLOR_RIGHT = '#E393F8'  # фиолетовый
COLOR_YTSUKEN_HIST = '#FF0000'   # Красный
COLOR_DIKTOR_HIST = '#FBFF00'    # Жёлтый
COLOR_VISOV_HIST = '#000000'     # Чёрный
COLOR_RUSFON_HIST = '#FFC0CB'    # Розовый
COLOR_SKOROPIS_HIST = '#FFA500'  # Оранжевый
COLOR_ZUBACHEV_HIST = '#4169E1'  # Синий
COLOR_ANT_HIST = '#ADDFAD'       # Зелёный

# --- ПРОГРАММА 1: ГИСТОГРАММА ---
def plot_finger_usage_bars(layout1, layout2, layout3, layout4, layout5, layout6, layout7, ax, main_title=""):
    """
    Рисует горизонтальную гистограмму на переданной оси `ax`.
    """
    fingers = ['Л_Большой', 'П_Большой', 'Л_Указательный', 'П_Указательный', 'Л_Средний', 'П_Средний',
               'Л_Безымянный', 'П_Безымянный', 'Л_Мизинец', 'П_Мизинец']
    
    color_skoropis = COLOR_SKOROPIS_HIST
    color_dictor = COLOR_DIKTOR_HIST
    color_visov = COLOR_VISOV_HIST
    color_ytsuken = COLOR_YTSUKEN_HIST
    color_rusfon = COLOR_RUSFON_HIST
    color_zubachev = COLOR_ZUBACHEV_HIST
    color_ant = COLOR_ANT_HIST

    index = np.arange(len(fingers))
    bar_width = 0.1  # уменьшили ширину, чтобы 7 столбцов поместились

    # Смещения для 7 раскладок
    offsets = [-3, -2, -1, 0, 1, 2, 3]
    layouts = [layout5, layout2, layout7, layout4, layout3, layout6, layout1]  # порядок: Русфон, Диктор, Ант, Йцукен, Вызов, Зубачев, Скоропись
    colors = [color_rusfon, color_dictor, color_ant, color_ytsuken, color_visov, color_zubachev, color_skoropis]
    labels = ['Русфон', 'Диктор', 'Ант', 'Йцукеи', 'Вызов', 'Зубачев', 'Скоропись']

    rects_list = []
    for i, (layout, color, label) in enumerate(zip(layouts, colors, labels)):
        rect = ax.barh(index + offsets[i] * bar_width, layout, bar_width, label=label, color=color, alpha=1.0)
        rects_list.append(rect)

    # Функция для добавления меток значений
    def add_labels(rects, ax, x_offset=50000):
        for rect in rects:
            width = rect.get_width()
            y_pos = rect.get_y() + rect.get_height() / 2
            ax.text(width + x_offset, y_pos, f'{int(width)}', va='center', ha='left', fontsize=6)

    for rects in rects_list:
        add_labels(rects, ax)

    ax.set_ylabel('Пальцы')
    ax.set_xlabel('Нагрузки (количество нажатий)')

    if main_title:
        ax.set_title(main_title)
    else:
        ax.set_title('Сравнение нагрузок на пальцы в раскладках йцукен, диктор, вызов, скоропись, русфон, зубачев и ант')

    ax.set_yticks(index)
    ax.set_yticklabels(fingers)
    
    all_values = layouts
    max_val = max(max(layout) for layout in all_values)
    ax.set_xlim(0, max_val * 1.15)
    ax.legend(loc='upper right', fontsize=8)

# --- ПРОГРАММА 2: КРУГОВЫЕ ДИАГРАММЫ ---
def create_single_pie_chart_internal(ax, values_left, values_right, color_left, color_right, labels, title):
    values = [values_left, values_right]
    colors = [color_left, color_right]

    wedges, texts, autotexts = ax.pie(
        values,
        labels=labels,
        colors=colors,
        autopct='%.1f%%',
        pctdistance=0.6,
        startangle=90,
        textprops={'fontsize': 9}
    )

    for text in autotexts:
        text.set_color('white')
        text.set_fontweight('bold')

    ax.set_title(title, fontsize=10, fontweight='bold')
    ax.axis('equal')

def create_and_plot_single_pie(data, title_prefix, ax, color_left, color_right):
    values_left = sum(data['left'])
    values_right = sum(data['right'])
    labels_for_pie = ['Л. Рука', 'П. Рука']
    create_single_pie_chart_internal(ax, values_left, values_right, color_left, color_right, labels_for_pie, title_prefix)

def create_pie_charts_on_axes(data_dictor, data_ytsuken, data_visov, data_skoropis,
                              data_rusfon, data_zubachev, data_ant, axes_list):
    pie_configs = [
        (data_dictor, "ДИКТОР", axes_list[0]),
        (data_ytsuken, "ЙЦУКЕН", axes_list[1]),
        (data_visov, "ВЫЗОВ", axes_list[2]),
        (data_skoropis, "Скоропись", axes_list[3]),
        (data_rusfon, "Русфон", axes_list[4]),
        (data_zubachev, "Зубачев", axes_list[5]),
        (data_ant, "Ант", axes_list[6])
    ]

    for data, title, ax in pie_configs:
        create_and_plot_single_pie(data, title, ax, COLOR_LEFT, COLOR_RIGHT)

# --- ОСНОВНАЯ ФУНКЦИЯ ---
def plot_combined_graphs(layout1, layout2, layout3, layout4, layout5, layout6, layout7,
                         data_dictor, data_ytsuken, data_visov, data_skoropis,
                         data_rusfon, data_zubachev, data_ant):
    # Создаём фигуру с GridSpec: 2 строки, 7 столбцов
    fig = plt.figure(figsize=(22, 10))
    gs = fig.add_gridspec(2, 7, height_ratios=[2, 1], hspace=0.4, wspace=0.3)

    # Гистограмма — вся верхняя строка
    ax_hist = fig.add_subplot(gs[0, :])

    # Круговые диаграммы — нижняя строка, 7 штук
    axes_pie = [fig.add_subplot(gs[1, i]) for i in range(7)]

    # Рисуем гистограмму
    plot_finger_usage_bars(layout1, layout2, layout3, layout4, layout5, layout6, layout7,
                           ax_hist, main_title="Сравнение нагрузок на пальцы")

    # Рисуем круговые диаграммы
    create_pie_charts_on_axes(data_dictor, data_ytsuken, data_visov, data_skoropis,
                              data_rusfon, data_zubachev, data_ant, axes_pie)

    # Общий заголовок
    fig.suptitle("Комплексный анализ нагрузок на пальцы по раскладкам", fontsize=16, fontweight='bold')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

# --- ВХОДНЫЕ ДАННЫЕ ---
layout1 = [336883, 224588, 1819640, 1300013, 685725, 231567, 161738, 73896, 401456, 293521]  # Йцукен
layout2 = [308809, 252662, 622693, 1208801, 247804, 574163, 225677, 506704, 205019, 407680]  # Диктор
layout3 = [280736, 280736, 654094, 693976, 908794, 384139, 195100, 148917, 264718, 354770]  # Вызов
layout4 = [280000, 280736, 654000, 693999, 908794, 388888, 195100, 144444, 264718, 354770]  # Йцукеи (уточнено)
layout5 = [430736, 890736, 654094, 223976, 308794, 384139, 105100, 118917, 404718, 604770]  # Русфон
layout6 = [170736, 300736, 804094, 203976, 408794, 204139, 505100, 908917, 264718, 354770]  # Зубачев
layout7 = [500736, 200736, 304094, 403976, 508794, 604139, 705100, 808917, 904718, 104770]  # Ант

data_dictor = {'left': [308809, 622693, 247804, 225677, 205019], 'right': [252662, 1208801, 574163, 506704, 407680]}
data_ytsuken = {'left': [336883, 1819640, 685725, 161738, 401456], 'right': [224588, 1300013, 231567, 73896, 293521]}
data_visov = {'left': [280736, 654094, 908794, 195100, 264718], 'right': [280736, 693976, 384139, 148917, 354770]}
data_skoropis = {'left': [280736, 654094, 908794, 195100, 264718], 'right': [280736, 693976, 384139, 148917, 354770]}
data_rusfon = {'left': [430736, 654094, 308794, 105100, 404718], 'right': [890736, 223976, 384139, 118917, 604770]}
data_zubachev = {'left': [170736, 804094, 408794, 505100, 264718], 'right': [300736, 203976, 204139, 908917, 354770]}
data_ant = {'left': [500736, 304094, 508794, 705100, 904718], 'right': [200736, 403976, 604139, 808917, 104770]}

# --- ЗАПУСК ---
if __name__ == "__main__":
    plot_combined_graphs(layout1, layout2, layout3, layout4, layout5, layout6, layout7,
                         data_dictor, data_ytsuken, data_visov, data_skoropis,
                         data_rusfon, data_zubachev, data_ant)
