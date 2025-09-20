"""
Модуль для экспорта результатов анализа в CSV файлы
"""
import csv
import os
from datetime import datetime
from typing import Dict, List, Any


def create_csv_report(result: Dict[str, Any], file_path: str, layout_name: str, 
                     output_dir: str = "reports") -> str:
    """
    Создает CSV отчет с результатами анализа
    
    Args:
        result: Результаты анализа
        file_path: Путь к анализируемому файлу
        layout_name: Название раскладки
        output_dir: Директория для сохранения отчетов
    
    Returns:
        str: Путь к созданному CSV файлу
    """
    # Создаем директорию для отчетов если её нет
    os.makedirs(output_dir, exist_ok=True)
    
    # Генерируем имя файла с временной меткой
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"analysis_report_{timestamp}.csv"
    csv_path = os.path.join(output_dir, csv_filename)
    
    # Подготавливаем данные для CSV
    report_data = [
        ["Параметр", "Значение"],
        ["Дата анализа", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        ["Анализируемый файл", file_path],
        ["Раскладка", layout_name],
        ["Тип анализа", result.get('text_type', 'words')],
        [""],
        ["=== ОСНОВНАЯ СТАТИСТИКА ===", ""],
        ["Общее количество ошибок", result['total_errors']],
        ["Обработано слов", result['total_words']],
        ["Всего символов", result['total_characters']],
        ["Обработано символов", result['processed_characters']],
        [""],
        ["=== СРЕДНИЕ ЗНАЧЕНИЯ ===", ""],
        ["Среднее ошибок на слово", f"{result['avg_errors_per_word']:.4f}"],
        ["Среднее ошибок на символ", f"{result['avg_errors_per_char']:.6f}"],
        [""],
        ["=== ПОКРЫТИЕ ===", ""],
        ["Покрытие раскладкой (%)", f"{(result['processed_characters'] / result['total_characters'] * 100):.2f}" if result['total_characters'] > 0 else "0.00"],
        ["Неизвестных символов", len(result['unknown_characters'])],
        [""],
        ["=== ОЦЕНКА КАЧЕСТВА ===", ""],
        ["Оценка", _get_quality_assessment(result['avg_errors_per_word'])],
    ]
    
    # Добавляем неизвестные символы если есть
    if result['unknown_characters']:
        report_data.extend([
            [""],
            ["=== НЕИЗВЕСТНЫЕ СИМВОЛЫ ===", ""],
        ])
        unknown_list = sorted(list(result['unknown_characters']))
        for i, char in enumerate(unknown_list[:50]):  # Первые 50 символов
            report_data.append([f"Символ {i+1}", repr(char)])
        
        if len(unknown_list) > 50:
            report_data.append([f"... и еще {len(unknown_list) - 50} символов", ""])
    
    # Записываем CSV файл
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(report_data)
    
    return csv_path


def create_detailed_csv_report(results_list: List[Dict[str, Any]], 
                              output_dir: str = "reports") -> str:
    """
    Создает детальный CSV отчет для сравнения нескольких анализов
    
    Args:
        results_list: Список результатов анализа
        output_dir: Директория для сохранения отчетов
    
    Returns:
        str: Путь к созданному CSV файлу
    """
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"detailed_comparison_{timestamp}.csv"
    csv_path = os.path.join(output_dir, csv_filename)
    
    # Заголовки для сравнительной таблицы
    headers = [
        "Файл", "Раскладка", "Тип анализа", "Дата",
        "Общие ошибки", "Слова", "Символы", "Обработано символов",
        "Ошибок/слово", "Ошибок/символ", "Покрытие %", "Неизвестных символов",
        "Оценка качества"
    ]
    
    rows = [headers]
    
    for result_data in results_list:
        result = result_data['result']
        coverage = (result['processed_characters'] / result['total_characters'] * 100) if result['total_characters'] > 0 else 0
        
        row = [
            result_data.get('file_path', 'N/A'),
            result_data.get('layout_name', 'N/A'),
            result.get('text_type', 'words'),
            result_data.get('timestamp', datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            result['total_errors'],
            result['total_words'],
            result['total_characters'],
            result['processed_characters'],
            f"{result['avg_errors_per_word']:.4f}",
            f"{result['avg_errors_per_char']:.6f}",
            f"{coverage:.2f}",
            len(result['unknown_characters']),
            _get_quality_assessment(result['avg_errors_per_word'])
        ]
        rows.append(row)
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)
    
    return csv_path


def _get_quality_assessment(avg_errors_per_word: float) -> str:
    """Возвращает текстовую оценку качества"""
    if avg_errors_per_word < 2:
        return "ОТЛИЧНО"
    elif avg_errors_per_word < 5:
        return "ХОРОШО"
    elif avg_errors_per_word < 10:
        return "СРЕДНЕ"
    else:
        return "ПЛОХО"


def export_unknown_characters_csv(unknown_chars: set, layout_name: str, 
                                 output_dir: str = "reports") -> str:
    """
    Экспортирует список неизвестных символов в отдельный CSV файл
    
    Args:
        unknown_chars: Множество неизвестных символов
        layout_name: Название раскладки
        output_dir: Директория для сохранения
    
    Returns:
        str: Путь к созданному файлу
    """
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"unknown_chars_{layout_name}_{timestamp}.csv"
    csv_path = os.path.join(output_dir, csv_filename)
    
    headers = ["Символ", "Unicode код", "Описание"]
    rows = [headers]
    
    for char in sorted(unknown_chars):
        unicode_code = f"U+{ord(char):04X}"
        try:
            import unicodedata
            description = unicodedata.name(char, "НЕИЗВЕСТНО")
        except:
            description = "НЕИЗВЕСТНО"
        
        rows.append([repr(char), unicode_code, description])
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)
    
    return csv_path


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
    
    csv_path = create_csv_report(
        result=sample_result,
        file_path="/path/to/test.txt",
        layout_name="test_layout"
    )
    print(f"Отчет создан: {csv_path}")