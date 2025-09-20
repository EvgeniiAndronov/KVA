import json
import csv
import os
from typing import Dict, Union, Any


def read_kl(filename: str) -> dict | None:
    """
    Универсальная функция для чтения раскладок из различных форматов
    Поддерживает: JSON, CSV, TXT (key:value), XML
    """
    if not os.path.exists(filename):
        print(f"❌ Файл не найден: {filename}")
        return None
    
    file_ext = os.path.splitext(filename)[1].lower()
    
    try:
        if file_ext == '.json':
            return _read_json_layout(filename)
        elif file_ext == '.csv':
            return _read_csv_layout(filename)
        elif file_ext in ['.txt', '.conf', '.cfg']:
            return _read_text_layout(filename)
        elif file_ext == '.xml':
            return _read_xml_layout(filename)
        else:
            # Пробуем автоопределение формата
            return _auto_detect_and_read(filename)
            
    except Exception as e:
        print(f"❌ Ошибка чтения файла раскладки: {e}")
        return None


def _read_json_layout(filename: str) -> dict:
    """
    Читает раскладку из JSON файла
    Ожидаемый формат: {"a": 1, "b": 2, ...} или {"layout": {"a": 1, "b": 2}}
    """
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Если есть вложенная структура, извлекаем раскладку
    if isinstance(data, dict):
        if 'layout' in data:
            return data['layout']
        elif 'keyboard_layout' in data:
            return data['keyboard_layout']
        elif 'rules' in data:
            return data['rules']
        else:
            # Проверяем, что все значения - числа
            if all(isinstance(v, (int, float)) for v in data.values()):
                return data
    
    raise ValueError("Неверный формат JSON файла раскладки")


def _read_csv_layout(filename: str) -> dict:
    """
    Читает раскладку из CSV файла
    Ожидаемые форматы:
    - letter,error
    - key,value
    - symbol,weight
    """
    layout = {}
    
    with open(filename, 'r', encoding='utf-8') as file:
        # Пробуем определить разделитель
        sample = file.read(1024)
        file.seek(0)
        
        delimiter = ',' if ',' in sample else ';' if ';' in sample else '\t'
        
        reader = csv.reader(file, delimiter=delimiter)
        
        # Пропускаем заголовок если есть
        first_row = next(reader, None)
        if first_row and not _is_numeric(first_row[1]):
            # Это заголовок, читаем дальше
            pass
        else:
            # Это данные, возвращаемся к началу
            file.seek(0)
            reader = csv.reader(file, delimiter=delimiter)
        
        for row in reader:
            if len(row) >= 2:
                key = row[0].strip()
                try:
                    value = float(row[1].strip())
                    layout[key] = value
                except ValueError:
                    continue
    
    return layout


def _read_text_layout(filename: str) -> dict:
    """
    Читает раскладку из текстового файла
    Поддерживаемые форматы:
    - key:value
    - key=value
    - key value
    - key\tvalue
    """
    layout = {}
    
    with open(filename, 'r', encoding='utf-8') as file:
        for line_num, line in enumerate(file, 1):
            line = line.strip()
            
            # Пропускаем пустые строки и комментарии
            if not line or line.startswith('#') or line.startswith('//'):
                continue
            
            # Пробуем различные разделители
            for separator in [':', '=', '\t', ' ']:
                if separator in line:
                    parts = line.split(separator, 1)
                    if len(parts) == 2:
                        key = parts[0].strip()
                        value_str = parts[1].strip()
                        
                        try:
                            value = float(value_str)
                            layout[key] = value
                            break
                        except ValueError:
                            continue
            else:
                print(f"⚠️  Не удалось разобрать строку {line_num}: {line}")
    
    return layout


def _read_xml_layout(filename: str) -> dict:
    """
    Читает раскладку из XML файла
    Ожидаемый формат:
    <layout>
        <key symbol="a" error="1"/>
        <key symbol="b" error="2"/>
    </layout>
    """
    try:
        import xml.etree.ElementTree as ET
    except ImportError:
        raise ImportError("Для чтения XML файлов требуется модуль xml.etree.ElementTree")
    
    layout = {}
    tree = ET.parse(filename)
    root = tree.getroot()
    
    # Ищем элементы с раскладкой
    for key_elem in root.findall('.//key'):
        symbol = key_elem.get('symbol') or key_elem.get('char') or key_elem.get('letter')
        error = key_elem.get('error') or key_elem.get('value') or key_elem.get('weight')
        
        if symbol and error:
            try:
                layout[symbol] = float(error)
            except ValueError:
                continue
    
    # Альтернативный формат
    if not layout:
        for elem in root.iter():
            if elem.text and elem.tag not in ['layout', 'keyboard']:
                try:
                    layout[elem.tag] = float(elem.text)
                except ValueError:
                    continue
    
    return layout


def _auto_detect_and_read(filename: str) -> dict:
    """
    Автоматически определяет формат файла и читает раскладку
    """
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read(1024)  # Читаем первые 1KB для анализа
        file.seek(0)
        full_content = file.read()
    
    # Проверяем на JSON
    if content.strip().startswith('{'):
        try:
            data = json.loads(full_content)
            return _extract_layout_from_dict(data)
        except json.JSONDecodeError:
            pass
    
    # Проверяем на XML
    if content.strip().startswith('<'):
        try:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(full_content)
            return _read_xml_layout(filename)
        except:
            pass
    
    # Проверяем на CSV (наличие запятых или точек с запятой)
    if ',' in content or ';' in content:
        try:
            return _read_csv_layout(filename)
        except:
            pass
    
    # По умолчанию пробуем как текстовый файл
    return _read_text_layout(filename)


def _extract_layout_from_dict(data: Any) -> dict:
    """Извлекает раскладку из словаря различной структуры"""
    if isinstance(data, dict):
        # Прямая раскладка
        if all(isinstance(v, (int, float)) for v in data.values()):
            return data
        
        # Вложенная структура
        for key in ['layout', 'keyboard_layout', 'rules', 'mapping', 'keys']:
            if key in data and isinstance(data[key], dict):
                return data[key]
    
    raise ValueError("Не удалось извлечь раскладку из структуры данных")


def _is_numeric(value: str) -> bool:
    """Проверяет, является ли строка числом"""
    try:
        float(value)
        return True
    except ValueError:
        return False


def save_layout_to_file(layout: dict, filename: str, format_type: str = 'json') -> bool:
    """
    Сохраняет раскладку в файл в указанном формате
    
    Args:
        layout: Словарь раскладки
        filename: Путь к файлу для сохранения
        format_type: Формат файла ('json', 'csv', 'txt', 'xml')
    
    Returns:
        bool: True если сохранение прошло успешно
    """
    try:
        if format_type.lower() == 'json':
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump({'layout': layout}, file, indent=2, ensure_ascii=False)
        
        elif format_type.lower() == 'csv':
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['symbol', 'error'])
                for key, value in sorted(layout.items()):
                    writer.writerow([key, value])
        
        elif format_type.lower() == 'txt':
            with open(filename, 'w', encoding='utf-8') as file:
                file.write("# Keyboard Layout Configuration\n")
                file.write("# Format: symbol:error_value\n\n")
                for key, value in sorted(layout.items()):
                    file.write(f"{key}:{value}\n")
        
        elif format_type.lower() == 'xml':
            with open(filename, 'w', encoding='utf-8') as file:
                file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                file.write('<layout>\n')
                for key, value in sorted(layout.items()):
                    file.write(f'  <key symbol="{key}" error="{value}"/>\n')
                file.write('</layout>\n')
        
        else:
            raise ValueError(f"Неподдерживаемый формат: {format_type}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка сохранения раскладки: {e}")
        return False


def validate_layout(layout: dict) -> tuple[bool, list]:
    """
    Валидирует раскладку на корректность
    
    Args:
        layout: Словарь раскладки для проверки
    
    Returns:
        tuple: (is_valid, list_of_errors)
    """
    errors = []
    
    if not isinstance(layout, dict):
        errors.append("Раскладка должна быть словарем")
        return False, errors
    
    if not layout:
        errors.append("Раскладка не может быть пустой")
        return False, errors
    
    for key, value in layout.items():
        if not isinstance(key, str):
            errors.append(f"Ключ '{key}' должен быть строкой")
        
        if not isinstance(value, (int, float)):
            errors.append(f"Значение для '{key}' должно быть числом, получено: {type(value)}")
        
        if isinstance(value, (int, float)) and value < 0:
            errors.append(f"Значение для '{key}' не может быть отрицательным: {value}")
    
    # Проверяем наличие основных символов
    basic_chars = set('abcdefghijklmnopqrstuvwxyz')
    layout_chars = set(layout.keys())
    missing_chars = basic_chars - layout_chars
    
    if len(missing_chars) > 10:  # Если отсутствует больше 10 базовых символов
        errors.append(f"Отсутствуют многие базовые символы: {sorted(list(missing_chars))[:10]}...")
    
    return len(errors) == 0, errors


if __name__ == "__main__":
    # Пример использования
    test_layout = {"a": 1, "b": 2, "c": 3}
    
    # Сохраняем в разных форматах
    save_layout_to_file(test_layout, "test_layout.json", "json")
    save_layout_to_file(test_layout, "test_layout.csv", "csv")
    save_layout_to_file(test_layout, "test_layout.txt", "txt")
    
    # Читаем обратно
    loaded = read_kl("test_layout.json")
    print(f"Загруженная раскладка: {loaded}")
    
    # Валидируем
    is_valid, errors = validate_layout(loaded)
    print(f"Валидация: {'✅' if is_valid else '❌'}")
    if errors:
        for error in errors:
            print(f"  - {error}")
