"""
Модуль для создания графиков и визуализации результатов анализа
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import os
from datetime import datetime
from typing import Dict, List, Any, Tuple
import sqlite3

# Импортируем новые функции для графиков пальцев
from data_module.finger_charts import (
    create_finger_pie_chart,
    create_finger_bar_chart,
    create_finger_comparison_chart,
    create_hand_load_pie_chart
)


def create_analysis_charts(result: Dict[str, Any], layout_name: str, file_path: str, 
                          output_dir: str = "reports") -> List[str]:
    """
    Создает набор графиков для анализа результатов
    
    Args:
        result: Результаты анализа
        layout_name: Название раскладки
        file_path: Путь к анализируемому файлу
        output_dir: Директория для сохранения графиков
    
    Returns:
        List[str]: Список путей к созданным графикам
    """
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    created_files = []
    
    # Настройка стиля matplotlib
    plt.style.use('default')
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['font.size'] = 10
    
    # Создаем только графики статистики пальцев (старые графики отключены)
    if 'finger_statistics' in result and result['finger_statistics']:
        finger_charts = create_finger_analysis_charts(result['finger_statistics'], layout_name, output_dir)
        created_files.extend(finger_charts)
    
    return created_files


def _create_coverage_pie_chart(result: Dict[str, Any], layout_name: str, 
                              timestamp: str, output_dir: str) -> str:
    """Создает круговую диаграмму покрытия символов"""
    try:
        processed = result['processed_characters']
        unknown = result['total_characters'] - processed
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        sizes = [processed, unknown]
        labels = [f'Обработано\n({processed:,} символов)', f'Неизвестно\n({unknown:,} символов)']
        colors = ['#2ecc71', '#e74c3c']
        explode = (0.05, 0)
        
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, explode=explode,
                                         autopct='%1.1f%%', startangle=90, shadow=True)
        
        # Улучшаем внешний вид
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(12)
        
        ax.set_title(f'Покрытие символов раскладкой "{layout_name}"', 
                    fontsize=16, fontweight='bold', pad=20)
        
        # Добавляем статистику
        coverage_percent = (processed / result['total_characters']) * 100
        plt.figtext(0.5, 0.02, f'Общее покрытие: {coverage_percent:.1f}% | '
                              f'Неизвестных символов: {len(result["unknown_characters"])}',
                   ha='center', fontsize=10, style='italic')
        
        filename = f"coverage_chart_{layout_name}_{timestamp}.png"
        filepath = os.path.join(output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath
    except Exception as e:
        print(f"Ошибка создания диаграммы покрытия: {e}")
        return None


def _create_error_distribution_chart(result: Dict[str, Any], layout_name: str, 
                                   timestamp: str, output_dir: str) -> str:
    """Создает гистограмму распределения ошибок"""
    try:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Левый график - основные метрики
        metrics = ['Общие ошибки', 'Слова', 'Символы', 'Обработано']
        values = [result['total_errors'], result['total_words'], 
                 result['total_characters'], result['processed_characters']]
        colors = ['#e74c3c', '#3498db', '#f39c12', '#2ecc71']
        
        bars1 = ax1.bar(metrics, values, color=colors, alpha=0.7)
        ax1.set_title('Основные метрики анализа', fontweight='bold')
        ax1.set_ylabel('Количество')
        
        # Добавляем значения на столбцы
        for bar, value in zip(bars1, values):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                    f'{value:,}', ha='center', va='bottom', fontweight='bold')
        
        # Правый график - средние значения
        avg_metrics = ['Ошибок/слово', 'Ошибок/символ']
        avg_values = [result['avg_errors_per_word'], result['avg_errors_per_char']]
        colors2 = ['#9b59b6', '#1abc9c']
        
        bars2 = ax2.bar(avg_metrics, avg_values, color=colors2, alpha=0.7)
        ax2.set_title('Средние значения', fontweight='bold')
        ax2.set_ylabel('Среднее количество ошибок')
        
        # Добавляем значения на столбцы
        for bar, value in zip(bars2, avg_values):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                    f'{value:.4f}', ha='center', va='bottom', fontweight='bold')
        
        plt.suptitle(f'Распределение ошибок - "{layout_name}"', 
                    fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        filename = f"error_distribution_{layout_name}_{timestamp}.png"
        filepath = os.path.join(output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath
    except Exception as e:
        print(f"Ошибка создания гистограммы: {e}")
        return None


def _create_metrics_comparison_chart(result: Dict[str, Any], layout_name: str, 
                                   timestamp: str, output_dir: str) -> str:
    """Создает сравнительную диаграмму метрик"""
    try:
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Создаем радарную диаграмму
        categories = ['Покрытие\n(%)', 'Качество\n(инверт)', 'Эффективность\n(%)', 
                     'Точность\n(%)', 'Полнота\n(%)']
        
        # Вычисляем метрики (нормализуем к 0-100)
        coverage = (result['processed_characters'] / result['total_characters']) * 100
        quality = max(0, 100 - result['avg_errors_per_word'] * 10)  # Инвертируем ошибки
        efficiency = min(100, (result['total_words'] / max(1, result['total_errors'])) * 100)
        accuracy = min(100, (result['processed_characters'] / max(1, result['total_characters'])) * 100)
        completeness = min(100, 100 - (len(result['unknown_characters']) / max(1, result['total_characters'])) * 10000)
        
        values = [coverage, quality, efficiency, accuracy, completeness]
        
        # Создаем радарную диаграмму
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        values += values[:1]  # Замыкаем диаграмму
        angles += angles[:1]
        
        ax = plt.subplot(111, projection='polar')
        ax.plot(angles, values, 'o-', linewidth=2, color='#3498db')
        ax.fill(angles, values, alpha=0.25, color='#3498db')
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        ax.set_ylim(0, 100)
        
        # Добавляем сетку
        ax.grid(True)
        ax.set_title(f'Комплексная оценка раскладки "{layout_name}"', 
                    fontsize=16, fontweight='bold', pad=30)
        
        # Добавляем легенду с значениями
        legend_text = f'Покрытие: {coverage:.1f}%\n' \
                     f'Качество: {quality:.1f}/100\n' \
                     f'Эффективность: {efficiency:.1f}%\n' \
                     f'Точность: {accuracy:.1f}%\n' \
                     f'Полнота: {completeness:.1f}%'
        
        plt.figtext(0.02, 0.02, legend_text, fontsize=10, 
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.8))
        
        filename = f"metrics_radar_{layout_name}_{timestamp}.png"
        filepath = os.path.join(output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath
    except Exception as e:
        print(f"Ошибка создания радарной диаграммы: {e}")
        return None


def create_history_comparison_chart(layout_name: str, output_dir: str = "reports") -> str:
    """
    Создает график сравнения истории анализов для раскладки
    
    Args:
        layout_name: Название раскладки
        output_dir: Директория для сохранения
    
    Returns:
        str: Путь к созданному графику
    """
    try:
        # Получаем данные из БД
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, count_errors, type_test 
            FROM data 
            WHERE name_lk = ? 
            ORDER BY id ASC
        """, (layout_name,))
        
        history = cursor.fetchall()
        conn.close()
        
        if len(history) < 2:
            print("Недостаточно данных для создания графика истории")
            return None
        
        # Подготавливаем данные
        test_numbers = list(range(1, len(history) + 1))
        errors = [record[1] for record in history]
        
        # Создаем график
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Верхний график - динамика ошибок
        ax1.plot(test_numbers, errors, 'o-', linewidth=2, markersize=6, color='#e74c3c')
        ax1.set_title(f'Динамика ошибок для раскладки "{layout_name}"', 
                     fontweight='bold', fontsize=14)
        ax1.set_xlabel('Номер теста')
        ax1.set_ylabel('Количество ошибок')
        ax1.grid(True, alpha=0.3)
        
        # Добавляем тренд
        if len(errors) > 1:
            z = np.polyfit(test_numbers, errors, 1)
            p = np.poly1d(z)
            ax1.plot(test_numbers, p(test_numbers), "--", alpha=0.8, color='#3498db',
                    label=f'Тренд: {"↓" if z[0] < 0 else "↑"} {abs(z[0]):.0f} ошибок/тест')
            ax1.legend()
        
        # Нижний график - гистограмма распределения
        ax2.hist(errors, bins=min(10, len(errors)), alpha=0.7, color='#2ecc71', edgecolor='black')
        ax2.set_title('Распределение количества ошибок', fontweight='bold', fontsize=14)
        ax2.set_xlabel('Количество ошибок')
        ax2.set_ylabel('Частота')
        ax2.grid(True, alpha=0.3)
        
        # Добавляем статистику
        avg_errors = np.mean(errors)
        std_errors = np.std(errors)
        ax2.axvline(avg_errors, color='red', linestyle='--', linewidth=2, 
                   label=f'Среднее: {avg_errors:.0f}')
        ax2.legend()
        
        plt.tight_layout()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"history_comparison_{layout_name}_{timestamp}.png"
        filepath = os.path.join(output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath
        
    except Exception as e:
        print(f"Ошибка создания графика истории: {e}")
        return None


def create_layouts_comparison_chart(output_dir: str = "reports") -> str:
    """
    Создает сравнительный график для всех раскладок
    
    Args:
        output_dir: Директория для сохранения
    
    Returns:
        str: Путь к созданному графику
    """
    try:
        # Получаем статистику по всем раскладкам
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT name_lk, 
                   COUNT(*) as tests_count,
                   AVG(count_errors) as avg_errors,
                   MIN(count_errors) as min_errors,
                   MAX(count_errors) as max_errors
            FROM data 
            WHERE name_lk NOT LIKE '%test%'
            GROUP BY name_lk
            HAVING tests_count >= 1
            ORDER BY avg_errors ASC
        """)
        
        layouts_data = cursor.fetchall()
        conn.close()
        
        if len(layouts_data) < 2:
            print("Недостаточно данных для сравнения раскладок")
            return None
        
        # Подготавливаем данные
        layout_names = [row[0] for row in layouts_data]
        avg_errors = [row[2] for row in layouts_data]
        min_errors = [row[3] for row in layouts_data]
        max_errors = [row[4] for row in layouts_data]
        tests_counts = [row[1] for row in layouts_data]
        
        # Создаем график
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # Левый график - сравнение средних ошибок
        bars = ax1.bar(layout_names, avg_errors, color='#3498db', alpha=0.7)
        ax1.set_title('Сравнение раскладок по среднему количеству ошибок', 
                     fontweight='bold', fontsize=14)
        ax1.set_ylabel('Среднее количество ошибок')
        ax1.tick_params(axis='x', rotation=45)
        
        # Добавляем значения на столбцы
        for bar, value, count in zip(bars, avg_errors, tests_counts):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                    f'{value:.0f}\n({count} тестов)', ha='center', va='bottom', fontsize=9)
        
        # Правый график - диапазон ошибок (min-max)
        x_pos = np.arange(len(layout_names))
        ax2.errorbar(x_pos, avg_errors, 
                    yerr=[np.array(avg_errors) - np.array(min_errors),
                          np.array(max_errors) - np.array(avg_errors)],
                    fmt='o', capsize=5, capthick=2, color='#e74c3c')
        
        ax2.set_title('Диапазон ошибок по раскладкам', fontweight='bold', fontsize=14)
        ax2.set_ylabel('Количество ошибок')
        ax2.set_xticks(x_pos)
        ax2.set_xticklabels(layout_names, rotation=45)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"layouts_comparison_{timestamp}.png"
        filepath = os.path.join(output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath
        
    except Exception as e:
        print(f"Ошибка создания сравнительного графика: {e}")
        return None


def create_finger_analysis_charts(finger_stats: Dict[str, int], layout_name: str, 
                                 output_dir: str = "reports") -> List[str]:
    """
    Создает набор графиков для анализа статистики пальцев
    
    Args:
        finger_stats: Словарь статистики пальцев {finger_code: press_count}
        layout_name: Название раскладки
        output_dir: Директория для сохранения графиков
    
    Returns:
        List[str]: Список путей к созданным графикам
    """
    if not finger_stats:
        return []
    
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    created_files = []
    
    try:
        # 1. Круговая диаграмма статистики пальцев
        pie_path = create_finger_pie_chart(
            finger_stats, 
            layout_name, 
            os.path.join(output_dir, f"finger_pie_{layout_name}_{timestamp}.png")
        )
        created_files.append(pie_path)
        
        # 2. Столбчатая диаграмма нагрузки на пальцы
        bar_path = create_finger_bar_chart(
            finger_stats, 
            layout_name, 
            os.path.join(output_dir, f"finger_bar_{layout_name}_{timestamp}.png")
        )
        created_files.append(bar_path)
        
        # 3. Диаграмма нагрузки на руки
        hand_path = create_hand_load_pie_chart(
            finger_stats, 
            layout_name, 
            os.path.join(output_dir, f"hand_load_{layout_name}_{timestamp}.png")
        )
        created_files.append(hand_path)
        
        print(f"✅ Создано {len(created_files)} графиков статистики пальцев")
        
    except Exception as e:
        print(f"❌ Ошибка создания графиков статистики пальцев: {e}")
    
    return created_files


def create_finger_comparison_charts(layouts_finger_stats: Dict[str, Dict[str, int]], 
                                  output_dir: str = "reports") -> List[str]:
    """
    Создает сравнительные графики статистики пальцев для нескольких раскладок
    
    Args:
        layouts_finger_stats: Словарь {layout_name: {finger_code: press_count}}
        output_dir: Директория для сохранения графиков
    
    Returns:
        List[str]: Список путей к созданным графикам
    """
    if not layouts_finger_stats or len(layouts_finger_stats) < 2:
        return []
    
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    created_files = []
    
    try:
        # Сравнительная диаграмма статистики пальцев
        comp_path = create_finger_comparison_chart(
            layouts_finger_stats,
            os.path.join(output_dir, f"finger_comparison_{timestamp}.png")
        )
        created_files.append(comp_path)
        
        print(f"✅ Создан сравнительный график статистики пальцев")
        
    except Exception as e:
        print(f"❌ Ошибка создания сравнительного графика: {e}")
    
    return created_files


if __name__ == "__main__":
    # Пример использования
    sample_result = {
        'total_errors': 1500,
        'total_words': 1000,
        'total_characters': 5000,
        'processed_characters': 4800,
        'unknown_characters': {'@', '#', '$'},
        'avg_errors_per_word': 1.5,
        'avg_errors_per_char': 0.0003,
        'text_type': 'words'
    }
    
    charts = create_analysis_charts(
        result=sample_result,
        layout_name="test_layout",
        file_path="/path/to/test.txt"
    )
    print(f"Созданы графики: {charts}")