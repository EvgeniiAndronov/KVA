#!/usr/bin/env python3
"""
Модуль для создания круговой диаграммы распределения по рукам
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, Optional
import os
from datetime import datetime

def create_hand_distribution_pie_chart(hand_data: Dict, layout_name: str, save_path: str = None) -> str:
    """
    Создает круговую диаграмму распределения по рукам (левая/правая/обе)
    
    Args:
        hand_data: Словарь с данными о руках
        layout_name: Название раскладки
        save_path: Путь для сохранения
    
    Returns:
        str: Путь к сохраненному файлу
    """
    
    # Извлекаем данные из структуры
    left_total = hand_data['left']['total']
    right_total = hand_data['right']['total'] 
    both_total = hand_data['both']['total']
    
    # Подготавливаем данные для диаграммы
    values = [left_total, right_total, both_total]
    labels = ['Левая рука', 'Правая рука', 'Обе руки']
    colors = ['#FF6B6B', '#C79FEF', '#96CEB4']  # Красный, бирюзовый, зеленый
    
    # Создаем диаграмму
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Вычисляем проценты
    total = sum(values)
    percentages = [(value / total * 100) if total > 0 else 0 for value in values]
    
    # Создаем круговую диаграмму
    wedges, texts, autotexts = ax.pie(
        values,
        labels=labels,
        colors=colors,
        autopct=lambda pct: f'{pct:.1f}%',
        startangle=90,
        textprops={'fontsize': 12}
    )
    
    # Улучшаем внешний вид
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    ax.set_title(f'Распределение нагрузки по рукам - {layout_name}', 
                fontsize=16, fontweight='bold', pad=20)
    
    # Добавляем легенду с количеством нажатий
    legend_labels = [f'{label}: {count:,}' for label, count in zip(labels, values)]
    ax.legend(wedges, legend_labels, title="Руки", loc="center left", 
             bbox_to_anchor=(1, 0, 0.5, 1), fontsize=11)
    
    plt.tight_layout()
    
    # Сохраняем файл
    if save_path is None:
        os.makedirs('charts/hand_stats', exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        save_path = f'charts/hand_stats/hand_distribution_{layout_name}_{timestamp}.png'
    
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return save_path

def create_comfort_hand_chart(hand_data: Dict, layout_name: str, save_path: str = None) -> str:
    """
    Создает круговую диаграмму комфортности по рукам
    
    Args:
        hand_data: Словарь с данными о руках
        layout_name: Название раскладки
        save_path: Путь для сохранения
    
    Returns:
        str: Путь к сохраненному файлу
    """
    
    # Извлекаем данные о комфортности для левой и правой руки
    left_comfort = hand_data['left']['comfortable']
    left_partial = hand_data['left']['partial']
    left_uncomfort = hand_data['left']['uncomfortable']
    
    right_comfort = hand_data['right']['comfortable']
    right_partial = hand_data['right']['partial']
    right_uncomfort = hand_data['right']['uncomfortable']
    
    # Суммируем по типам комфортности
    total_comfort = left_comfort + right_comfort
    total_partial = left_partial + right_partial
    total_uncomfort = left_uncomfort + right_uncomfort
    
    # Подготавливаем данные для диаграммы
    values = [total_comfort, total_partial, total_uncomfort]
    labels = ['Удобные', 'Частично удобные', 'Неудобные']
    colors = ['#4ECDC4', '#FFEAA7', '#FF6B6B']  # Зеленый, желтый, красный
    
    # Создаем диаграмму
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Вычисляем проценты
    total = sum(values)
    percentages = [(value / total * 100) if total > 0 else 0 for value in values]
    
    # Создаем круговую диаграмму
    wedges, texts, autotexts = ax.pie(
        values,
        labels=labels,
        colors=colors,
        autopct=lambda pct: f'{pct:.1f}%',
        startangle=90,
        textprops={'fontsize': 12}
    )
    
    # Улучшаем внешний вид
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    ax.set_title(f'Удобность нажатий (левая + правая рука) - {layout_name}', 
                fontsize=16, fontweight='bold', pad=20)
    
    # Добавляем легенду с количеством нажатий
    legend_labels = [f'{label}: {count:,}' for label, count in zip(labels, values)]
    ax.legend(wedges, legend_labels, title="Типы нажатий", loc="center left", 
             bbox_to_anchor=(1, 0, 0.5, 1), fontsize=11)
    
    plt.tight_layout()
    
    # Сохраняем файл
    if save_path is None:
        os.makedirs('charts/hand_stats', exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        save_path = f'charts/hand_stats/comfort_hand_{layout_name}_{timestamp}.png'
    
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return save_path

# Пример использования с данными из файла
if __name__ == "__main__":
    # Данные из прикрепленного файла
    hand_data = {
      "left": {
        "total": 3257960,
        "comfortable": 667244,
        "partial": 678646,
        "uncomfortable": 1912070,
        "comfortable_percent": 20.48042333239205,
        "partial_percent": 20.830396935505654,
        "uncomfortable_percent": 58.68917973210229
      },
      "right": {
        "total": 2167475,
        "comfortable": 341441,
        "partial": 260956,
        "uncomfortable": 1565078,
        "comfortable_percent": 15.75293832685498,
        "partial_percent": 12.039631368297213,
        "uncomfortable_percent": 72.2074303048478
      },
      "both": {
        "total": 18288774,
        "comfortable": 0,
        "partial": 0,
        "uncomfortable": 18288774,
        "comfortable_percent": 0.0,
        "partial_percent": 0.0,
        "uncomfortable_percent": 100.0
      }
    }
    
    layout_name = "Йцукен"
    
    # Создаем папку для графиков
    os.makedirs('charts/hand_stats', exist_ok=True)
    
    try:
        # Создаем диаграмму распределения по рукам
        dist_path = create_hand_distribution_pie_chart(hand_data, layout_name)
        print(f"✅ Диаграмма распределения по рукам создана: {dist_path}")
        
        # Создаем диаграмму комфортности
        comfort_path = create_comfort_hand_chart(hand_data, layout_name)
        print(f"✅ Диаграмма комфортности создана: {comfort_path}")
        
        print(f"\n📊 Статистика:")
        print(f"Левая рука: {hand_data['left']['total']:,} нажатий")
        print(f"Правая рука: {hand_data['right']['total']:,} нажатий") 
        print(f"Обе руки: {hand_data['both']['total']:,} нажатий")
        print(f"Всего: {hand_data['left']['total'] + hand_data['right']['total'] + hand_data['both']['total']:,} нажатий")
        
    except Exception as e:
        print(f"❌ Ошибка при создании графиков: {e}")