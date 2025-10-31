from tqdm import tqdm
from typing import Generator, List, Dict, Union


def make_processing(wordlist: list, rules: dict) -> dict:
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
    finger_stats = {}  # Статистика по пальцам
    
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
                    
                    # Собираем статистику по пальцам
                    if finger in finger_stats:
                        finger_stats[finger] += 1
                    else:
                        finger_stats[finger] = 1
                else:
                    # Неверный формат данных
                    unknown_characters.add(letter)
            else:
                unknown_characters.add(letter)
    
    return {
        'total_errors': mistakes,
        'total_words': len(wordlist),
        'total_characters': total_characters,
        'processed_characters': processed_characters,
        'unknown_characters': unknown_characters,
        'finger_statistics': finger_stats,
        'avg_errors_per_word': mistakes / len(wordlist) if wordlist else 0,
        'avg_errors_per_char': mistakes / processed_characters if processed_characters else 0
    }


def make_processing_stream(wordlist_generator: Generator[List[str], None, None], 
                          rules: Dict[str, Union[int, float, List]], 
                          total_words: int = None) -> dict:
    """
    Обрабатывает большие файлы батчами с прогресс-баром.
    
    Args:
        wordlist_generator: Генератор батчей слов
        rules: Словарь правил для подсчета ошибок
        total_words: Общее количество слов для прогресс-бара (опционально)
    
    Returns:
        dict: Словарь с результатами анализа
    """
    mistakes = 0
    processed_words = 0
    total_characters = 0
    processed_characters = 0
    unknown_characters = set()
    finger_stats = {}  # Статистика по пальцам
    
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
                        
                        # Поддерживаем оба формата: старый (число) и новый (список)
                        if isinstance(rule_data, (int, float)):
                            # Старый формат: только штраф
                            batch_mistakes += rule_data
                            processed_characters += 1
                            batch_processed_chars += 1
                        elif isinstance(rule_data, list) and len(rule_data) >= 2:
                            # Новый формат: [штраф, палец]
                            penalty, finger = rule_data[0], rule_data[1]
                            batch_mistakes += penalty
                            processed_characters += 1
                            batch_processed_chars += 1
                            
                            # Собираем статистику по пальцам
                            if finger in finger_stats:
                                finger_stats[finger] += 1
                            else:
                                finger_stats[finger] = 1
                        else:
                            # Неверный формат данных
                            unknown_characters.add(letter)
                    else:
                        unknown_characters.add(letter)
            
            mistakes += batch_mistakes
            processed_words += len(batch)
            pbar.update(len(batch))
            
            # Обновляем описание с текущими результатами
            avg_per_word = mistakes / processed_words if processed_words else 0
            pbar.set_postfix({
                'ошибки': mistakes, 
                'слов': processed_words,
                'ср/слово': f'{avg_per_word:.1f}'
            })
    
    finally:
        pbar.close()
    
    return {
        'total_errors': mistakes,
        'total_words': processed_words,
        'total_characters': total_characters,
        'processed_characters': processed_characters,
        'unknown_characters': unknown_characters,
        'finger_statistics': finger_stats,
        'avg_errors_per_word': mistakes / processed_words if processed_words else 0,
        'avg_errors_per_char': mistakes / processed_characters if processed_characters else 0
    }


def validate_rules(rules: Dict[str, Union[int, float, List]]) -> bool:
    """
    Проверяет корректность словаря правил.
    Поддерживает как старый формат (число), так и новый ([штраф, палец]).
    
    Args:
        rules: Словарь правил для проверки
        
    Returns:
        True если правила корректны
        
    Raises:
        ValueError: Если правила некорректны
    """
    if not isinstance(rules, dict):
        raise ValueError("Правила должны быть словарем")
    
    if not rules:
        raise ValueError("Словарь правил не может быть пустым")
    
    for key, value in rules.items():
        if not isinstance(key, str):
            raise ValueError(f"Ключ правила должен быть строкой, получен: {type(key)}")
        
        # Проверяем старый формат (число)
        if isinstance(value, (int, float)):
            if value < 0:
                raise ValueError(f"Значение правила не может быть отрицательным: {value}")
        
        # Проверяем новый формат (список)
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

#/home/evgenii/develop/PyProj/KVA/test_words.txt
#/home/evgenii/develop/PyProj/KVA/rockyou.txt


def make_text_processing(text: str, rules: dict) -> dict:
    """
    Считает количество ошибок по словарю правил для сплошного текста.
    ВНИМАНИЕ: Используйте только для небольших текстов!
    
    Returns:
        dict: Словарь с результатами анализа
    """
    if len(text) > 100000:  # 100KB текста
        raise ValueError(f"Текст слишком большой ({len(text)} символов). Используйте make_text_processing_stream()")
    
    mistakes = 0
    total_characters = len(text)
    processed_characters = 0
    unknown_characters = set()
    finger_stats = {}  # Статистика по пальцам
    
    print(f"Обрабатываем текст из {total_characters:,} символов...")
    
    for char in tqdm(text, desc="Обработка символов"):
        if char in rules:
            rule_data = rules[char]
            
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
                
                # Собираем статистику по пальцам
                if finger in finger_stats:
                    finger_stats[finger] += 1
                else:
                    finger_stats[finger] = 1
            else:
                # Неверный формат данных
                unknown_characters.add(char)
        else:
            unknown_characters.add(char)
    
    # Подсчитываем слова (приблизительно)
    words = text.split()
    word_count = len(words)
    
    return {
        'total_errors': mistakes,
        'total_words': word_count,
        'total_characters': total_characters,
        'processed_characters': processed_characters,
        'unknown_characters': unknown_characters,
        'finger_statistics': finger_stats,
        'avg_errors_per_word': mistakes / word_count if word_count else 0,
        'avg_errors_per_char': mistakes / processed_characters if processed_characters else 0,
        'text_type': 'continuous'
    }


def make_text_processing_stream(text_generator: Generator[str, None, None], 
                               rules: Dict[str, Union[int, float, List]], 
                               total_chars: int = None) -> dict:
    """
    Обрабатывает большие текстовые файлы чанками с прогресс-баром.
    
    Args:
        text_generator: Генератор чанков текста
        rules: Словарь правил для подсчета ошибок
        total_chars: Общее количество символов для прогресс-бара (опционально)
    
    Returns:
        dict: Словарь с результатами анализа
    """
    mistakes = 0
    processed_characters = 0
    total_characters = 0
    unknown_characters = set()
    finger_stats = {}  # Статистика по пальцам
    word_count = 0
    
    # Создаем прогресс-бар
    if total_chars:
        pbar = tqdm(total=total_chars, desc="Обработка текста", unit="символ")
    else:
        pbar = tqdm(desc="Обработка текста", unit="символ")
    
    try:
        for chunk in text_generator:
            chunk_mistakes = 0
            chunk_processed = 0
            
            # Подсчитываем слова в чанке
            word_count += len(chunk.split())
            
            for char in chunk:
                total_characters += 1
                if char in rules:
                    rule_data = rules[char]
                    
                    # Поддерживаем оба формата: старый (число) и новый (список)
                    if isinstance(rule_data, (int, float)):
                        # Старый формат: только штраф
                        chunk_mistakes += rule_data
                        processed_characters += 1
                        chunk_processed += 1
                    elif isinstance(rule_data, list) and len(rule_data) >= 2:
                        # Новый формат: [штраф, палец]
                        penalty, finger = rule_data[0], rule_data[1]
                        chunk_mistakes += penalty
                        processed_characters += 1
                        chunk_processed += 1
                        
                        # Собираем статистику по пальцам
                        if finger in finger_stats:
                            finger_stats[finger] += 1
                        else:
                            finger_stats[finger] = 1
                    else:
                        # Неверный формат данных
                        unknown_characters.add(char)
                else:
                    unknown_characters.add(char)
            
            mistakes += chunk_mistakes
            pbar.update(len(chunk))
            
            # Обновляем описание с текущими результатами
            avg_per_char = mistakes / processed_characters if processed_characters else 0
            pbar.set_postfix({
                'ошибки': mistakes,
                'символы': total_characters,
                'ср/симв': f'{avg_per_char:.3f}'
            })
    
    finally:
        pbar.close()
    
    return {
        'total_errors': mistakes,
        'total_words': word_count,
        'total_characters': total_characters,
        'processed_characters': processed_characters,
        'unknown_characters': unknown_characters,
        'finger_statistics': finger_stats,
        'avg_errors_per_word': mistakes / word_count if word_count else 0,
        'avg_errors_per_char': mistakes / processed_characters if processed_characters else 0,
        'text_type': 'continuous'
    }