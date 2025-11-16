from tqdm import tqdm
from typing import Generator, List, Dict, Union, Tuple
from collections import defaultdict
import sqlite3


def save_to_database(results: dict, db_path: str = "database.db"):
    """
    Сохраняет результаты анализа в базу данных.
    
    Args:
        results: Результаты анализа из функций make_processing*
        db_path: Путь к файлу базы данных
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Создаем таблицу если она не существует
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data_to_diograms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_lk TEXT NOT NULL,
            count_errors REAL,
            count_tap_bl INTEGER,
            count_tap_bl_e REAL,
            count_tap_bp INTEGER,
            count_tap_bp_e REAL,
            count_tap_ly INTEGER,
            count_tap_ly_e REAL,
            count_tap_py INTEGER,
            count_tap_py_e REAL,
            count_tap_ls INTEGER,
            count_tap_ls_e REAL,
            count_tap_ps INTEGER,
            count_tap_ps_e REAL,
            count_tap_lb INTEGER,
            count_tap_lb_e REAL,
            count_tap_pb INTEGER,
            count_tap_pb_e REAL,
            count_tap_lm INTEGER,
            count_tap_lm_e REAL,
            count_tap_pm INTEGER,
            count_tap_pm_e REAL
        )
    ''')
    
    # Маппинг названий пальцев на названия столбцов
    finger_mapping = {
        'bl': ('count_tap_bl', 'count_tap_bl_e'),  # Большой левый
        'bp': ('count_tap_bp', 'count_tap_bp_e'),  # Большой правый
        'ly': ('count_tap_ly', 'count_tap_ly_e'),  # Указательный левый
        'py': ('count_tap_py', 'count_tap_py_e'),  # Указательный правый
        'ls': ('count_tap_ls', 'count_tap_ls_e'),  # Средний левый
        'ps': ('count_tap_ps', 'count_tap_ps_e'),  # Средний правый
        'lb': ('count_tap_lb', 'count_tap_lb_e'),  # Безымянный левый
        'pb': ('count_tap_pb', 'count_tap_pb_e'),  # Безымянный правый
        'lm': ('count_tap_lm', 'count_tap_lm_e'),  # Мизинец левый
        'pm': ('count_tap_pm', 'count_tap_pm_e')   # Мизинец правый
    }
    
    # Подготавливаем данные для вставки
    layout_name = results.get('layout_name', 'unknown')
    total_errors = results.get('total_errors', 0)
    
    # Инициализируем значения для всех пальцев нулями
    insert_data = {
        'name_lk': layout_name,
        'count_errors': total_errors
    }
    
    for finger, (tap_col, error_col) in finger_mapping.items():
        insert_data[tap_col] = results.get('finger_statistics', {}).get(finger, 0)
        insert_data[error_col] = results.get('finger_errors', {}).get(finger, 0)
    
    # Вставляем данные
    cursor.execute('''
        INSERT INTO data_to_diograms 
        (name_lk, count_errors, 
         count_tap_bl, count_tap_bl_e, count_tap_bp, count_tap_bp_e,
         count_tap_ly, count_tap_ly_e, count_tap_py, count_tap_py_e,
         count_tap_ls, count_tap_ls_e, count_tap_ps, count_tap_ps_e,
         count_tap_lb, count_tap_lb_e, count_tap_pb, count_tap_pb_e,
         count_tap_lm, count_tap_lm_e, count_tap_pm, count_tap_pm_e)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        insert_data['name_lk'], insert_data['count_errors'],
        insert_data['count_tap_bl'], insert_data['count_tap_bl_e'],
        insert_data['count_tap_bp'], insert_data['count_tap_bp_e'],
        insert_data['count_tap_ly'], insert_data['count_tap_ly_e'],
        insert_data['count_tap_py'], insert_data['count_tap_py_e'],
        insert_data['count_tap_ls'], insert_data['count_tap_ls_e'],
        insert_data['count_tap_ps'], insert_data['count_tap_ps_e'],
        insert_data['count_tap_lb'], insert_data['count_tap_lb_e'],
        insert_data['count_tap_pb'], insert_data['count_tap_pb_e'],
        insert_data['count_tap_lm'], insert_data['count_tap_lm_e'],
        insert_data['count_tap_pm'], insert_data['count_tap_pm_e']
    ))
    
    conn.commit()
    conn.close()
    
    print(f"Данные для раскладки '{layout_name}' успешно сохранены в базу")


def make_processing(wordlist: list, rules: dict, layout_name: str = "unknown", save_to_db: bool = True) -> dict:
    """
    Считает количество ошибок по словарю правил и списку слов.
    ВНИМАНИЕ: Используйте только для небольших списков!
    
    Returns:
        dict: Словарь с результатами анализа
    """
    if len(wordlist) > 10000:
        raise ValueError(f"Список слишком большой ({len(wordlist)} слов). Используйте make_processing_stream()")
    
    mistakes = 0
    total_characters = 0
    processed_characters = 0
    unknown_characters = set()
    
    # Расширенная статистика по пальцам
    finger_stats = defaultdict(int)  # Общее количество нажатий каждого пальца
    finger_errors = defaultdict(float)  # Количество ошибок на каждый палец
    finger_data = {}  # Детальная информация по каждому пальцу
    
    print(f"Обрабатываем {len(wordlist)} слов...")
    
    for word in tqdm(wordlist, desc="Обработка слов"):
        for letter in word:
            total_characters += 1
            if letter in rules:
                rule_data = rules[letter]
                
                # Поддерживаем оба формата: старый (число) и новый (список)
                if isinstance(rule_data, (int, float)):
                    # Старый формат: только штраф
                    mistakes += rule_data
                    processed_characters += 1
                elif isinstance(rule_data, list) and len(rule_data) >= 2:
                    # Новый формат: [штраф, палец]
                    penalty, finger = rule_data[0], rule_data[1]
                    mistakes += penalty
                    processed_characters += 1
                    
                    # Собираем расширенную статистику по пальцам
                    finger_stats[finger] += 1
                    finger_errors[finger] += penalty
                    
                    # Сохраняем детальную информацию о пальце
                    if finger not in finger_data:
                        finger_data[finger] = {
                            'total_presses': 0,
                            'total_errors': 0.0,
                            'error_rate': 0.0
                        }
                    finger_data[finger]['total_presses'] += 1
                    finger_data[finger]['total_errors'] += penalty
                    
                else:
                    # Неверный формат данных
                    unknown_characters.add(letter)
            else:
                unknown_characters.add(letter)
    
    # Рассчитываем процент ошибок для каждого пальца
    for finger in finger_data:
        total_presses = finger_data[finger]['total_presses']
        total_errors = finger_data[finger]['total_errors']
        finger_data[finger]['error_rate'] = total_errors / total_presses if total_presses > 0 else 0
    
    results = {
        'total_errors': mistakes,
        'total_words': len(wordlist),
        'total_characters': total_characters,
        'processed_characters': processed_characters,
        'unknown_characters': unknown_characters,
        'finger_statistics': dict(finger_stats),
        'finger_errors': dict(finger_errors),
        'finger_detailed_data': finger_data,
        'layout_name': layout_name,
        'avg_errors_per_word': mistakes / len(wordlist) if wordlist else 0,
        'avg_errors_per_char': mistakes / processed_characters if processed_characters else 0
    }
    
    # Сохраняем в базу данных если требуется
    if save_to_db:
        save_to_database(results)
    
    return results


def make_processing_stream(wordlist_generator: Generator[List[str], None, None], 
                          rules: Dict[str, Union[int, float, List]], 
                          total_words: int = None,
                          layout_name: str = "unknown",
                          save_to_db: bool = True) -> dict:
    """
    Обрабатывает большие файлы батчами с прогресс-баром.
    """
    mistakes = 0
    processed_words = 0
    total_characters = 0
    processed_characters = 0
    unknown_characters = set()
    
    # Расширенная статистика по пальцам
    finger_stats = defaultdict(int)  # Общее количество нажатий каждого пальца
    finger_errors = defaultdict(float)  # Количество ошибок на каждый палец
    finger_data = {}  # Детальная информация по каждому пальцу
    
    # Создаем прогресс-бар
    if total_words:
        pbar = tqdm(total=total_words, desc="Обработка слов")
    else:
        pbar = tqdm(desc="Обработка слов")
    
    try:
        for batch in wordlist_generator:
            batch_mistakes = 0
            batch_chars = 0
            batch_processed_chars = 0
            
            for word in batch:
                for letter in word:
                    total_characters += 1
                    batch_chars += 1
                    if letter in rules:
                        rule_data = rules[letter]
                        
                        if isinstance(rule_data, (int, float)):
                            batch_mistakes += rule_data
                            processed_characters += 1
                            batch_processed_chars += 1
                        elif isinstance(rule_data, list) and len(rule_data) >= 2:
                            penalty, finger = rule_data[0], rule_data[1]
                            batch_mistakes += penalty
                            processed_characters += 1
                            batch_processed_chars += 1
                            
                            finger_stats[finger] += 1
                            finger_errors[finger] += penalty
                            
                            if finger not in finger_data:
                                finger_data[finger] = {
                                    'total_presses': 0,
                                    'total_errors': 0.0,
                                    'error_rate': 0.0
                                }
                            finger_data[finger]['total_presses'] += 1
                            finger_data[finger]['total_errors'] += penalty
                            
                        else:
                            unknown_characters.add(letter)
                    else:
                        unknown_characters.add(letter)
            
            mistakes += batch_mistakes
            processed_words += len(batch)
            pbar.update(len(batch))
            
            avg_per_word = mistakes / processed_words if processed_words else 0
            pbar.set_postfix({
                'ошибки': mistakes, 
                'слов': processed_words,
                'ср/слово': f'{avg_per_word:.1f}'
            })
    
    finally:
        pbar.close()
    
    # Рассчитываем процент ошибок для каждого пальца
    for finger in finger_data:
        total_presses = finger_data[finger]['total_presses']
        total_errors = finger_data[finger]['total_errors']
        finger_data[finger]['error_rate'] = total_errors / total_presses if total_presses > 0 else 0
    
    results = {
        'total_errors': mistakes,
        'total_words': processed_words,
        'total_characters': total_characters,
        'processed_characters': processed_characters,
        'unknown_characters': unknown_characters,
        'finger_statistics': dict(finger_stats),
        'finger_errors': dict(finger_errors),
        'finger_detailed_data': finger_data,
        'layout_name': layout_name,
        'avg_errors_per_word': mistakes / processed_words if processed_words else 0,
        'avg_errors_per_char': mistakes / processed_characters if processed_characters else 0
    }
    
    # Сохраняем в базу данных если требуется
    if save_to_db:
        save_to_database(results)
    
    return results


def make_text_processing(text: str, rules: dict, layout_name: str = "unknown", save_to_db: bool = True) -> dict:
    """
    Считает количество ошибок по словарю правил для сплошного текста.
    ВНИМАНИЕ: Используйте только для небольших текстов!
    """
    if len(text) > 100000:
        raise ValueError(f"Текст слишком большой ({len(text)} символов). Используйте make_text_processing_stream()")
    
    mistakes = 0
    total_characters = len(text)
    processed_characters = 0
    unknown_characters = set()
    
    # Расширенная статистика по пальцам
    finger_stats = defaultdict(int)
    finger_errors = defaultdict(float)
    finger_data = {}
    
    print(f"Обрабатываем текст из {total_characters:,} символов...")
    
    for char in tqdm(text, desc="Обработка символов"):
        if char in rules:
            rule_data = rules[char]
            
            if isinstance(rule_data, (int, float)):
                mistakes += rule_data
                processed_characters += 1
            elif isinstance(rule_data, list) and len(rule_data) >= 2:
                penalty, finger = rule_data[0], rule_data[1]
                mistakes += penalty
                processed_characters += 1
                
                finger_stats[finger] += 1
                finger_errors[finger] += penalty
                
                if finger not in finger_data:
                    finger_data[finger] = {
                        'total_presses': 0,
                        'total_errors': 0.0,
                        'error_rate': 0.0
                    }
                finger_data[finger]['total_presses'] += 1
                finger_data[finger]['total_errors'] += penalty
                
            else:
                unknown_characters.add(char)
        else:
            unknown_characters.add(char)
    
    words = text.split()
    word_count = len(words)
    
    for finger in finger_data:
        total_presses = finger_data[finger]['total_presses']
        total_errors = finger_data[finger]['total_errors']
        finger_data[finger]['error_rate'] = total_errors / total_presses if total_presses > 0 else 0
    
    results = {
        'total_errors': mistakes,
        'total_words': word_count,
        'total_characters': total_characters,
        'processed_characters': processed_characters,
        'unknown_characters': unknown_characters,
        'finger_statistics': dict(finger_stats),
        'finger_errors': dict(finger_errors),
        'finger_detailed_data': finger_data,
        'layout_name': layout_name,
        'avg_errors_per_word': mistakes / word_count if word_count else 0,
        'avg_errors_per_char': mistakes / processed_characters if processed_characters else 0,
        'text_type': 'continuous'
    }
    
    if save_to_db:
        save_to_database(results)
    
    return results


def make_text_processing_stream(text_generator: Generator[str, None, None], 
                               rules: Dict[str, Union[int, float, List]], 
                               total_chars: int = None,
                               layout_name: str = "unknown",
                               save_to_db: bool = True) -> dict:
    """
    Обрабатывает большие текстовые файлы чанками с прогресс-баром.
    """
    mistakes = 0
    processed_characters = 0
    total_characters = 0
    unknown_characters = set()
    
    finger_stats = defaultdict(int)
    finger_errors = defaultdict(float)
    finger_data = {}
    word_count = 0
    
    if total_chars:
        pbar = tqdm(total=total_chars, desc="Обработка текста", unit="символ")
    else:
        pbar = tqdm(desc="Обработка текста", unit="символ")
    
    try:
        for chunk in text_generator:
            chunk_mistakes = 0
            chunk_processed = 0
            
            word_count += len(chunk.split())
            
            for char in chunk:
                total_characters += 1
                if char in rules:
                    rule_data = rules[char]
                    
                    if isinstance(rule_data, (int, float)):
                        chunk_mistakes += rule_data
                        processed_characters += 1
                        chunk_processed += 1
                    elif isinstance(rule_data, list) and len(rule_data) >= 2:
                        penalty, finger = rule_data[0], rule_data[1]
                        chunk_mistakes += penalty
                        processed_characters += 1
                        chunk_processed += 1
                        
                        finger_stats[finger] += 1
                        finger_errors[finger] += penalty
                        
                        if finger not in finger_data:
                            finger_data[finger] = {
                                'total_presses': 0,
                                'total_errors': 0.0,
                                'error_rate': 0.0
                            }
                        finger_data[finger]['total_presses'] += 1
                        finger_data[finger]['total_errors'] += penalty
                        
                    else:
                        unknown_characters.add(char)
                else:
                    unknown_characters.add(char)
            
            mistakes += chunk_mistakes
            pbar.update(len(chunk))
            
            avg_per_char = mistakes / processed_characters if processed_characters else 0
            pbar.set_postfix({
                'ошибки': mistakes,
                'символы': total_characters,
                'ср/симв': f'{avg_per_char:.3f}'
            })
    
    finally:
        pbar.close()
    
    for finger in finger_data:
        total_presses = finger_data[finger]['total_presses']
        total_errors = finger_data[finger]['total_errors']
        finger_data[finger]['error_rate'] = total_errors / total_presses if total_presses > 0 else 0
    
    results = {
        'total_errors': mistakes,
        'total_words': word_count,
        'total_characters': total_characters,
        'processed_characters': processed_characters,
        'unknown_characters': unknown_characters,
        'finger_statistics': dict(finger_stats),
        'finger_errors': dict(finger_errors),
        'finger_detailed_data': finger_data,
        'layout_name': layout_name,
        'avg_errors_per_word': mistakes / word_count if word_count else 0,
        'avg_errors_per_char': mistakes / processed_characters if processed_characters else 0,
        'text_type': 'continuous'
    }
    
    if save_to_db:
        save_to_database(results)
    
    return results


# Функция validate_rules остается без изменений
def validate_rules(rules: Dict[str, Union[int, float, List]]) -> bool:
    """
    Проверяет корректность словаря правил.
    Поддерживает как старый формат (число), так и новый ([штраф, палец]).
    """
    if not isinstance(rules, dict):
        raise ValueError("Правила должны быть словарем")
    
    if not rules:
        raise ValueError("Словарь правил не может быть пустым")
    
    for key, value in rules.items():
        if not isinstance(key, str):
            raise ValueError(f"Ключ правила должен быть строкой, получен: {type(key)}")
        
        if isinstance(value, (int, float)):
            if value < 0:
                raise ValueError(f"Значение правила не может быть отрицательным: {value}")
        
        elif isinstance(value, list):
            if len(value) < 2:
                raise ValueError(f"Список правила должен содержать минимум 2 элемента [штраф, палец], получено: {len(value)}")
            
            penalty, finger = value[0], value[1]
            
            if not isinstance(penalty, (int, float)):
                raise ValueError(f"Штраф должен быть числом, получено: {type(penalty)}")
            
            if penalty < 0:
                raise ValueError(f"Штраф не может быть отрицательным: {penalty}")
            
            if not isinstance(finger, str):
                raise ValueError(f"Палец должен быть строкой, получено: {type(finger)}")
            
            if not finger.strip():
                raise ValueError("Палец не может быть пустой строкой")
        
        else:
            raise ValueError(f"Значение правила должно быть числом или списком [штраф, палец], получено: {type(value)}")
    
    return True