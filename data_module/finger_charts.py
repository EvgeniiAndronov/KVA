#!/usr/bin/env python3
"""
Модуль для создания графиков статистики пальцев на основе реальных данных анализа
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Optional
import os
from datetime import datetime

# Константы цветов
FINGER_COLORS = {
    'pb': '#FF6B6B',  # Красный - левый большой
    'rb': '#4ECDC4',  # Бирюзовый - правый большой  
    'ps': '#45B7D1',  # Синий - левый указательный
    'rs': '#96CEB4',  # Зеленый - правый указательный
    'pm': '#FFEAA7',  # Желтый - левый средний
    'rm': '#DDA0DD',  # Сиреневый - правый средний
    'pr': '#FFB347',  # Оранжевый - левый безымянный
    'rr': '#F8BBD9',  # Розовый - правый безымянный
    'pl': '#C7CEEA',  # Лавандовый - левый мизинец
    'rl': '#B4E7CE',  # Мятный - правый мизинец
    'bl': '#A8E6CF',  # Светло-зеленый - пробел (большие пальцы)
    
    # Дополнительные коды пальцев из примеров
    'ly': '#FF6B6B',  # левый указательный
    'ry': '#96CEB4',  # правый указательный
    'lm': '#FFEAA7',  # левый средний
    'ls': '#45B7D1',  # левый указательный (альтернативный)
    'py': '#DDA0DD',  # правый средний (альтернативный)
    'lb': '#C7CEEA',  # левый безымянный
}

# Маппинг кодов пальцев на понятные названия
# Логика: первая буква = рука (l-левая, p-правая), вторая = палец (y-указательный, s-средний, b-безымянный, m-мизинец)
FINGER_NAMES = {
    # Левая рука (l префикс)
    'ly': 'Л.Указательный',
    'ls': 'Л.Средний', 
    'lb': 'Л.Безымянный',
    'lm': 'Л.Мизинец',
    
    # Правая рука (p префикс)
    'py': 'П.Указательный',
    'ps': 'П.Средний',
    'pb': 'П.Безымянный', 
    'pm': 'П.Мизинец',
    
    # Правая рука (r префикс - альтернативный)
    'ry': 'П.Указательный',
    'rs': 'П.Средний',
    'rb': 'П.Безымянный',
    'rm': 'П.Мизинец',
    
    # Специальные
    'bl': 'Пробел',
}


def create_finger_pie_chart(finger_stats: Dict[str, int], layout_name: str, save_path: str = None) -> str:
    """
    Создает круговую диаграмму статистики пальцев
    
    Args:
        finger_stats: Словарь {finger_code: press_count}
        layout_name: Название раскладки
        save_path: Путь для сохранения (если None, создается автоматически)
    
    Returns:
        str: Путь к сохраненному файлу
    """
    if not finger_stats:
        raise ValueError("Нет данных для построения диаграммы")
    
    # Подготавливаем данные
    fingers = list(finger_stats.keys())
    counts = list(finger_stats.values())
    colors = [FINGER_COLORS.get(finger, '#CCCCCC') for finger in fingers]
    labels = [FINGER_NAMES.get(finger, finger) for finger in fingers]
    
    # Создаем диаграмму
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Вычисляем проценты
    total = sum(counts)
    percentages = [(count / total * 100) if total > 0 else 0 for count in counts]
    
    # Создаем круговую диаграмму
    wedges, texts, autotexts = ax.pie(
        counts,
        labels=labels,
        colors=colors,
        autopct=lambda pct: f'{pct:.1f}%' if pct > 2 else '',  # Показываем проценты только если > 2%
        startangle=90,
        textprops={'fontsize': 10}
    )
    
    # Улучшаем внешний вид
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    ax.set_title(f'Статистика нажатий пальцев - {layout_name}', 
                fontsize=16, fontweight='bold', pad=20)
    
    # Добавляем легенду с количеством нажатий
    legend_labels = [f'{label}: {count:,}' for label, count in zip(labels, counts)]
    ax.legend(wedges, legend_labels, title="Пальцы", loc="center left", 
             bbox_to_anchor=(1, 0, 0.5, 1), fontsize=9)
    
    plt.tight_layout()
    
    # Сохраняем файл
    if save_path is None:
        os.makedirs('charts/finger_stats', exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        save_path = f'charts/finger_stats/finger_pie_{layout_name}_{timestamp}.png'
    
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return save_path


def create_finger_bar_chart(finger_stats: Dict[str, int], layout_name: str, save_path: str = None) -> str:
    """
    Создает столбчатую диаграмму статистики пальцев
    
    Args:
        finger_stats: Словарь {finger_code: press_count}
        layout_name: Название раскладки
        save_path: Путь для сохранения
    
    Returns:
        str: Путь к сохраненному файлу
    """
    if not finger_stats:
        raise ValueError("Нет данных для построения диаграммы")
    
    # Сортируем по количеству нажатий (по убыванию)
    sorted_items = sorted(finger_stats.items(), key=lambda x: x[1], reverse=True)
    fingers = [item[0] for item in sorted_items]
    counts = [item[1] for item in sorted_items]
    colors = [FINGER_COLORS.get(finger, '#CCCCCC') for finger in fingers]
    labels = [FINGER_NAMES.get(finger, finger) for finger in fingers]
    
    # Создаем диаграмму
    fig, ax = plt.subplots(figsize=(14, 8))
    
    bars = ax.bar(labels, counts, color=colors, alpha=0.8, edgecolor='black', linewidth=0.5)
    
    # Добавляем значения на столбцы
    for bar, count in zip(bars, counts):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + max(counts) * 0.01,
                f'{count:,}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    ax.set_title(f'Нагрузка на пальцы - {layout_name}', 
                fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Пальцы', fontsize=12)
    ax.set_ylabel('Количество нажатий', fontsize=12)
    
    # Поворачиваем подписи по оси X
    plt.xticks(rotation=45, ha='right')
    
    # Добавляем сетку
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_axisbelow(True)
    
    plt.tight_layout()
    
    # Сохраняем файл
    if save_path is None:
        os.makedirs('charts/finger_stats', exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        save_path = f'charts/finger_stats/finger_bar_{layout_name}_{timestamp}.png'
    
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return save_path


def create_finger_comparison_chart(layouts_stats: Dict[str, Dict[str, int]], save_path: str = None) -> str:
    """
    Создает сравнительную диаграмму статистики пальцев для нескольких раскладок
    
    Args:
        layouts_stats: Словарь {layout_name: {finger_code: press_count}}
        save_path: Путь для сохранения
    
    Returns:
        str: Путь к сохраненному файлу
    """
    if not layouts_stats:
        raise ValueError("Нет данных для сравнения")
    
    # Собираем все уникальные пальцы
    all_fingers = set()
    for stats in layouts_stats.values():
        all_fingers.update(stats.keys())
    
    all_fingers = sorted(list(all_fingers))
    finger_labels = [FINGER_NAMES.get(finger, finger) for finger in all_fingers]
    
    # Подготавливаем данные для каждой раскладки
    layout_names = list(layouts_stats.keys())
    n_layouts = len(layout_names)
    n_fingers = len(all_fingers)
    
    # Создаем диаграмму
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # Ширина столбцов и позиции
    bar_width = 0.8 / n_layouts
    index = np.arange(n_fingers)
    
    colors = plt.cm.Set3(np.linspace(0, 1, n_layouts))
    
    # Рисуем столбцы для каждой раскладки
    for i, layout_name in enumerate(layout_names):
        stats = layouts_stats[layout_name]
        counts = [stats.get(finger, 0) for finger in all_fingers]
        
        offset = (i - n_layouts/2 + 0.5) * bar_width
        bars = ax.bar(index + offset, counts, bar_width, 
                     label=layout_name, color=colors[i], alpha=0.8)
        
        # Добавляем значения на столбцы (только если они не слишком маленькие)
        max_count = max(counts) if counts else 0
        for bar, count in zip(bars, counts):
            if count > max_count * 0.05:  # Показываем только если больше 5% от максимума
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + max_count * 0.01,
                       f'{count:,}', ha='center', va='bottom', fontsize=7, rotation=90)
    
    ax.set_title('Сравнение нагрузки на пальцы по раскладкам', 
                fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Пальцы', fontsize=12)
    ax.set_ylabel('Количество нажатий', fontsize=12)
    ax.set_xticks(index)
    ax.set_xticklabels(finger_labels, rotation=45, ha='right')
    
    # Добавляем легенду
    ax.legend(loc='upper right')
    
    # Добавляем сетку
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_axisbelow(True)
    
    plt.tight_layout()
    
    # Сохраняем файл
    if save_path is None:
        os.makedirs('charts/finger_stats', exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        save_path = f'charts/finger_stats/finger_comparison_{timestamp}.png'
    
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return save_path


def create_hand_load_pie_chart(finger_stats: Dict[str, int], layout_name: str, save_path: str = None) -> str:
    """
    Создает круговую диаграмму нагрузки на руки (левая/правая)
    
    Args:
        finger_stats: Словарь {finger_code: press_count}
        layout_name: Название раскладки
        save_path: Путь для сохранения
    
    Returns:
        str: Путь к сохраненному файлу
    """
    if not finger_stats:
        raise ValueError("Нет данных для построения диаграммы")
    
    # Разделяем на левую и правую руку
    # Логика: первая буква = рука (l-левая, p-правая), вторая = палец (y-указательный, s-средний, b-безымянный, m-мизинец)
    left_hand = 0
    right_hand = 0
    both_hands = 0
    
    for finger, count in finger_stats.items():
        if '+' in finger:  # Двуручные комбинации (например, "lb+pm")
            both_hands += count
        elif finger == 'bl':  # Пробел (обе руки)
            both_hands += count
        elif len(finger) >= 2:
            first_char = finger[0].lower()
            if first_char == 'l':  # Левая рука (ly, ls, lb, lm, etc.)
                left_hand += count
            elif first_char == 'p':  # Правая рука (py, ps, pb, pm, etc.)
                right_hand += count
            elif first_char == 'r':  # Правая рука (ry, rs, rb, rm, etc.) - альтернативный код
                right_hand += count
            else:
                # Неизвестный код, относим к обеим рукам
                both_hands += count
        else:
            # Односимвольные коды относим к обеим рукам
            both_hands += count
    
    # Создаем диаграмму
    values = [left_hand, right_hand, both_hands]
    labels = ['Левая рука', 'Правая рука', 'Обе руки']
    colors = ['#B5DECF', '#EEE78E', '#E383EF']
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Убираем нулевые значения
    non_zero_data = [(val, label, color) for val, label, color in zip(values, labels, colors) if val > 0]
    if not non_zero_data:
        raise ValueError("Все значения равны нулю")
    
    values, labels, colors = zip(*non_zero_data)
    
    wedges, texts, autotexts = ax.pie(
        values,
        labels=labels,
        colors=colors,
        autopct='%1.1f%%',
        startangle=90,
        textprops={'fontsize': 12}
    )
    
    # Улучшаем внешний вид
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    ax.set_title(f'Нагрузка на руки - {layout_name}', 
                fontsize=16, fontweight='bold', pad=20)
    
    # Добавляем легенду с количеством нажатий
    legend_labels = [f'{label}: {count:,}' for label, count in zip(labels, values)]
    ax.legend(wedges, legend_labels, title="Руки", loc="center left", 
             bbox_to_anchor=(1, 0, 0.5, 1), fontsize=11)
    
    plt.tight_layout()
    
    # Сохраняем файл
    if save_path is None:
        os.makedirs('charts/finger_stats', exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        save_path = f'charts/finger_stats/hand_load_{layout_name}_{timestamp}.png'
    
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return save_path


# Пример использования (для тестирования)
if __name__ == "__main__":
    # Тестовые данные
    test_finger_stats = {
        'py': 38,
        'ls': 20, 
        'ly': 19,
        'ps': 16,
        'lb': 14,
        'lm': 11,
        'pb': 10,
        'pm': 8
    }
    
    test_layout_name = "test_layout"
    
    # Создаем папку для тестов
    os.makedirs('charts/finger_stats', exist_ok=True)
    
    try:
        # Тестируем круговую диаграмму
        pie_path = create_finger_pie_chart(test_finger_stats, test_layout_name)
        print(f"✅ Круговая диаграмма создана: {pie_path}")
        
        # Тестируем столбчатую диаграмму
        bar_path = create_finger_bar_chart(test_finger_stats, test_layout_name)
        print(f"✅ Столбчатая диаграмма создана: {bar_path}")
        
        # Тестируем диаграмму нагрузки на руки
        hand_path = create_hand_load_pie_chart(test_finger_stats, test_layout_name)
        print(f"✅ Диаграмма нагрузки на руки создана: {hand_path}")
        
        # Тестируем сравнительную диаграмму
        test_comparison_data = {
            "Layout1": test_finger_stats,
            "Layout2": {'py': 25, 'ls': 30, 'ly': 15, 'ps': 20, 'lb': 18}
        }
        comp_path = create_finger_comparison_chart(test_comparison_data)
        print(f"✅ Сравнительная диаграмма создана: {comp_path}")
        
    except Exception as e:
        print(f"❌ Ошибка при создании графиков: {e}")