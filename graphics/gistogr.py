import matplotlib.pyplot as plt
import numpy as np

def plot_hand_comparison(
    left_data,      # данные левой руки
    right_data,     # данные правой руки  
    labels,         # названия категорий
    title="Сравнение рук",
    left_name="Левая рука",
    right_name="Правая рука",
    colors=('#008080', '#FF6347')
):
    """
    Простая горизонтальная гистограмма сравнения
    """
    # Проверка данных
    if len(left_data) != len(labels) or len(right_data) != len(labels):
        raise ValueError("Несовпадение размеров данных и меток")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    y = np.arange(len(labels))
    height = 0.35
    
    # Столбцы
    left_bars = ax.barh(y - height/2, left_data, height, 
                       label=left_name, color=colors[0], alpha=0.8)
    right_bars = ax.barh(y + height/2, right_data, height, 
                        label=right_name, color=colors[1], alpha=0.8)
    
    # Подписи значений
    for bars in [left_bars, right_bars]:
        for bar in bars:
            width = bar.get_width()
            ax.text(width + max(max(left_data), max(right_data)) * 0.01,
                   bar.get_y() + bar.get_height()/2,
                   f'{width:.0f}', va='center', fontsize=9)
    
    # Настройки осей
    
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlabel('Количество')
    ax.set_title(title, fontweight='bold')
    
    # Сетка и легенда
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.legend()
    
    # Автомасштаб
    max_val = max(max(left_data), max(right_data))
    ax.set_xlim(0, max_val * 1.15)
    
    plt.tight_layout()
    plt.show()
    return fig, ax

# Пример использования
if __name__ == "__main__":
    categories = ["2 символа", "3 символа", "4 символа", "5 символов"]
    left = [172326, 28216, 1194, 7]
    right = [137860,22572, 955, 2]
    
    plot_hand_comparison(left, right, categories, "Количество удобных переборов йцукен") 