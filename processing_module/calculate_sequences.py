from typing import Dict, List, Tuple, Set, Any, Generator, Iterator
import json
from collections import defaultdict, Counter
import math
import os

class LayoutAnalyzer:
    def __init__(self, layout_config: Dict[str, Any]):
        """
        Инициализация анализатора раскладки
        
        Args:
            layout_config: Конфигурация раскладки в формате JSON
        """
        self.layout_data = layout_config.get("layout", {})
        self.hand_map = {}  # Буква -> рука
        self.position_map = {}  # Буква -> (рука, строка, столбец)
        self.finger_map = {}  # Буква -> палец (на основе столбца)
        
        self._parse_layout()
    
    def _parse_layout(self):
        """Парсит конфигурацию раскладки и создает маппинги"""
        for letter, data in self.layout_data.items():
            if len(data) >= 3:
                hand, row, col = data[0], data[1], data[2]
                self.hand_map[letter] = hand
                self.position_map[letter] = (hand, row, col)
                
                # Определяем палец на основе столбца
                finger = self._get_finger_for_column(hand, col)
                self.finger_map[letter] = finger
    
    def _get_finger_for_column(self, hand: str, column: int) -> str:
        """
        Определяет палец для столбца
        Логика: 
        - Столбцы 1-2: указательный палец
        - Столбцы 3-4: средний палец  
        - Столбцы 5-6: безымянный палец
        - Столбцы 7+: мизинец
        """
        if column <= 2:
            return f"{hand}y"  # указательный
        elif column <= 4:
            return f"{hand}s"  # средний
        elif column <= 6:
            return f"{hand}b"  # безымянный
        else:
            return f"{hand}m"  # мизинец

    # ... остальные методы класса (analyze_word_sequences, _classify_sequence, etc.) остаются без изменений ...
    def analyze_word_sequences(self, word: str) -> Dict[str, Any]:
        """
        Анализирует последовательности в слове
        
        Returns:
            Словарь с характеристиками последовательностей
        """
        if len(word) < 2:
            return {
                'total_sequences': 0,
                'hand_changes': 0,
                'direction_changes': 0,
                'same_hand_sequences': 0,
                'same_finger_sequences': 0,
                'sequence_analysis': []
            }
        
        sequences = []
        hand_changes = 0
        direction_changes = 0
        same_hand_sequences = 0
        same_finger_sequences = 0
        
        # Анализируем все последовательности длиной 2
        for i in range(len(word) - 1):
            seq = word[i:i+2]
            char1, char2 = seq[0], seq[1]
            
            if char1 not in self.hand_map or char2 not in self.hand_map:
                continue
                
            hand1 = self.hand_map[char1]
            hand2 = self.hand_map[char2]
            finger1 = self.finger_map.get(char1, '')
            finger2 = self.finger_map.get(char2, '')
            
            # Определяем тип последовательности
            sequence_type = self._classify_sequence(char1, char2)
            sequences.append({
                'sequence': seq,
                'type': sequence_type,
                'hand1': hand1,
                'hand2': hand2,
                'finger1': finger1,
                'finger2': finger2
            })
            
            # Считаем статистику
            if hand1 != hand2:
                hand_changes += 1
            else:
                same_hand_sequences += 1
                
            if finger1 == finger2:
                same_finger_sequences += 1
        
        # Анализируем направление (для последовательностей из 3+ символов)
        for i in range(len(word) - 2):
            seq = word[i:i+3]
            if all(c in self.position_map for c in seq):
                direction_change = self._check_direction_change(seq)
                direction_changes += direction_change
        
        return {
            'total_sequences': len(sequences),
            'hand_changes': hand_changes,
            'direction_changes': direction_changes,
            'same_hand_sequences': same_hand_sequences,
            'same_finger_sequences': same_finger_sequences,
            'sequence_analysis': sequences
        }
    
    def _classify_sequence(self, char1: str, char2: str) -> str:
        """
        Классифицирует последовательность из 2 символов
        """
        if char1 not in self.position_map or char2 not in self.position_map:
            return "unknown"
        
        hand1, row1, col1 = self.position_map[char1]
        hand2, row2, col2 = self.position_map[char2]
        
        if hand1 != hand2:
            return "hand_change"  # Смена руки - удобно
        
        # Одна рука
        finger1 = self.finger_map[char1]
        finger2 = self.finger_map[char2]
        
        if finger1 == finger2:
            return "same_finger"  # Один палец - неудобно
        
        # Проверяем направление
        row_diff = row2 - row1
        col_diff = col2 - col1
        
        if (row_diff > 0 and col_diff > 0) or (row_diff < 0 and col_diff < 0):
            return "same_direction"  # Одно направление - удобно
        else:
            return "direction_change"  # Смена направления - частично удобно
    
    def _check_direction_change(self, sequence: str) -> int:
        """
        Проверяет смену направления в последовательности из 3+ символов
        Returns: 1 если есть смена направления, иначе 0
        """
        positions = [self.position_map[char] for char in sequence if char in self.position_map]
        if len(positions) < 3:
            return 0
        
        directions = []
        for i in range(len(positions) - 1):
            hand1, row1, col1 = positions[i]
            hand2, row2, col2 = positions[i+1]
            
            if hand1 == hand2:  # Только для одной руки
                row_dir = 1 if row2 > row1 else (-1 if row2 < row1 else 0)
                col_dir = 1 if col2 > col1 else (-1 if col2 < col1 else 0)
                directions.append((row_dir, col_dir))
        
        # Проверяем смену направления
        for i in range(len(directions) - 1):
            if directions[i] != directions[i+1]:
                return 1
        
        return 0
    
    def calculate_layout_comfort(self, wordlist: List[str]) -> Dict[str, Any]:
        """
        Рассчитывает общую удобность раскладки для списка слов
        """
        total_sequences = 0
        total_hand_changes = 0
        total_direction_changes = 0
        total_same_hand = 0
        total_same_finger = 0
        
        sequence_types = Counter()
        word_analyses = []
        
        for word in wordlist:
            analysis = self.analyze_word_sequences(word)
            word_analyses.append({
                'word': word,
                'analysis': analysis
            })
            
            total_sequences += analysis['total_sequences']
            total_hand_changes += analysis['hand_changes']
            total_direction_changes += analysis['direction_changes']
            total_same_hand += analysis['same_hand_sequences']
            total_same_finger += analysis['same_finger_sequences']
            
            # Считаем типы последовательностей
            for seq_analysis in analysis['sequence_analysis']:
                sequence_types[seq_analysis['type']] += 1
        
        # Рассчитываем проценты
        total_analyzed_pairs = total_sequences
        
        if total_analyzed_pairs > 0:
            hand_change_percent = (total_hand_changes / total_analyzed_pairs) * 100
            direction_change_percent = (total_direction_changes / total_analyzed_pairs) * 100
            same_hand_percent = (total_same_hand / total_analyzed_pairs) * 100
            same_finger_percent = (total_same_finger / total_analyzed_pairs) * 100
        else:
            hand_change_percent = direction_change_percent = same_hand_percent = same_finger_percent = 0
        
        # Оценка удобности (чем выше, тем удобнее)
        comfort_score = (
            hand_change_percent * 1.0 +  # Смена руки - очень хорошо
            same_hand_percent * 0.3 +    # Одна рука - нормально
            -same_finger_percent * 0.5   # Один палец - плохо
        )
        
        return {
            'total_words': len(wordlist),
            'total_character_pairs': total_sequences,
            'comfort_score': comfort_score,
            'percentages': {
                'hand_changes': hand_change_percent,
                'direction_changes': direction_change_percent,
                'same_hand': same_hand_percent,
                'same_finger': same_finger_percent
            },
            'absolute_counts': {
                'hand_changes': total_hand_changes,
                'direction_changes': total_direction_changes,
                'same_hand_sequences': total_same_hand,
                'same_finger_sequences': total_same_finger
            },
            'sequence_type_distribution': dict(sequence_types),
            'word_analyses': word_analyses
        }

    def calculate_layout_comfort_stream(self, wordlist_generator: Generator[List[str], None, None], 
                                      total_words: int = None) -> Dict[str, Any]:
        """
        Рассчитывает удобность раскладки для потокового генератора слов
        
        Args:
            wordlist_generator: Генератор, возвращающий батчи слов
            total_words: Общее количество слов (для прогресс-бара)
        """
        from tqdm import tqdm
        
        total_sequences = 0
        total_hand_changes = 0
        total_direction_changes = 0
        total_same_hand = 0
        total_same_finger = 0
        processed_words = 0
        
        sequence_types = Counter()
        
        # Создаем прогресс-бар
        if total_words:
            pbar = tqdm(total=total_words, desc="Анализ удобности")
        else:
            pbar = tqdm(desc="Анализ удобности")
        
        try:
            for batch in wordlist_generator:
                batch_sequences = 0
                batch_hand_changes = 0
                batch_direction_changes = 0
                batch_same_hand = 0
                batch_same_finger = 0
                
                for word in batch:
                    analysis = self.analyze_word_sequences(word)
                    
                    batch_sequences += analysis['total_sequences']
                    batch_hand_changes += analysis['hand_changes']
                    batch_direction_changes += analysis['direction_changes']
                    batch_same_hand += analysis['same_hand_sequences']
                    batch_same_finger += analysis['same_finger_sequences']
                    
                    # Считаем типы последовательностей
                    for seq_analysis in analysis['sequence_analysis']:
                        sequence_types[seq_analysis['type']] += 1
                
                total_sequences += batch_sequences
                total_hand_changes += batch_hand_changes
                total_direction_changes += batch_direction_changes
                total_same_hand += batch_same_hand
                total_same_finger += batch_same_finger
                processed_words += len(batch)
                
                pbar.update(len(batch))
                pbar.set_postfix({
                    'слов': processed_words,
                    'пар_символов': total_sequences
                })
        
        finally:
            pbar.close()
        
        # Рассчитываем проценты
        total_analyzed_pairs = total_sequences
        
        if total_analyzed_pairs > 0:
            hand_change_percent = (total_hand_changes / total_analyzed_pairs) * 100
            direction_change_percent = (total_direction_changes / total_analyzed_pairs) * 100
            same_hand_percent = (total_same_hand / total_analyzed_pairs) * 100
            same_finger_percent = (total_same_finger / total_analyzed_pairs) * 100
        else:
            hand_change_percent = direction_change_percent = same_hand_percent = same_finger_percent = 0
        
        # Оценка удобности
        comfort_score = (
            hand_change_percent * 1.0 +
            same_hand_percent * 0.3 +
            -same_finger_percent * 0.5
        )
        
        return {
            'total_words': processed_words,
            'total_character_pairs': total_sequences,
            'comfort_score': comfort_score,
            'percentages': {
                'hand_changes': hand_change_percent,
                'direction_changes': direction_change_percent,
                'same_hand': same_hand_percent,
                'same_finger': same_finger_percent
            },
            'absolute_counts': {
                'hand_changes': total_hand_changes,
                'direction_changes': total_direction_changes,
                'same_hand_sequences': total_same_hand,
                'same_finger_sequences': total_same_finger
            },
            'sequence_type_distribution': dict(sequence_types)
        }
    
    def generate_comfort_rules(self) -> Dict[str, List]:
        """
        Генерирует правила удобности для использования с make_processing
        на основе анализа раскладки
        """
        rules = {}
        
        for letter in self.layout_data.keys():
            # Базовый штраф 0, будет корректироваться в зависимости от контекста
            finger = self.finger_map.get(letter, 'unknown')
            rules[letter] = [0.0, finger]
        
        return rules


# Функции для работы с файлами
def load_layout_from_json(file_path: str) -> Dict[str, Any]:
    """
    Загружает конфигурацию раскладки из JSON файла
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def read_words_by_lines(file_path: str, batch_size: int = 1000, 
                       encoding: str = 'utf-8') -> Generator[List[str], None, None]:
    """
    Читает файл построчно, возвращая батчи слов
    
    Args:
        file_path: Путь к файлу
        batch_size: Размер батча (количество строк за раз)
        encoding: Кодировка файла
    
    Yields:
        Списки слов из batch_size строк
    """
    current_batch = []
    
    with open(file_path, 'r', encoding=encoding) as f:
        for line in f:
            line = line.strip()
            if line:  # Пропускаем пустые строки
                # Разбиваем строку на слова
                words = line.split()
                current_batch.extend(words)
                
                # Возвращаем батч когда накопили достаточно
                if len(current_batch) >= batch_size:
                    yield current_batch
                    current_batch = []
    
    # Возвращаем остаток
    if current_batch:
        yield current_batch


def read_text_by_chunks(file_path: str, chunk_size: int = 8192,
                       encoding: str = 'utf-8') -> Generator[str, None, None]:
    """
    Читает текстовый файл (как роман) чанками фиксированного размера
    
    Args:
        file_path: Путь к файлу
        chunk_size: Размер чанка в байтах
        encoding: Кодировка файла
    
    Yields:
        Текстовые чанки
    """
    with open(file_path, 'r', encoding=encoding) as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk


def count_lines_in_file(file_path: str, encoding: str = 'utf-8') -> int:
    """
    Считает количество строк в файле (для прогресс-бара)
    """
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            return sum(1 for _ in f)
    except:
        return 0


def count_approximate_words_in_file(file_path: str, encoding: str = 'utf-8') -> int:
    """
    Приблизительно считает количество слов в файле (для прогресс-бара)
    """
    try:
        word_count = 0
        with open(file_path, 'r', encoding=encoding) as f:
            for line in f:
                word_count += len(line.split())
        return word_count
    except:
        return 0


# Основные функции анализа
def analyze_layout_comfort(layout_config: Dict[str, Any], wordlist: List[str]) -> Dict[str, Any]:
    """
    Основная функция для анализа удобности раскладки (для небольших списков)
    """
    analyzer = LayoutAnalyzer(layout_config)
    return analyzer.calculate_layout_comfort(wordlist)


def analyze_layout_comfort_from_file(layout_config: Dict[str, Any], 
                                   file_path: str, 
                                   file_type: str = 'words',
                                   batch_size: int = 1000,
                                   encoding: str = 'utf-8') -> Dict[str, Any]:
    """
    Анализирует удобность раскладки из файла
    
    Args:
        layout_config: Конфигурация раскладки
        file_path: Путь к файлу
        file_type: 'words' для списка слов, 'text' для сплошного текста
        batch_size: Размер батча для обработки
        encoding: Кодировка файла
    """
    analyzer = LayoutAnalyzer(layout_config)
    
    if file_type == 'words':
        # Файл со списком слов (по одному слову на строку)
        total_words = count_lines_in_file(file_path, encoding)
        word_generator = read_words_by_lines(file_path, batch_size, encoding)
        return analyzer.calculate_layout_comfort_stream(word_generator, total_words)
    
    elif file_type == 'text':
        # Сплошной текст (роман, статья и т.д.)
        total_words = count_approximate_words_in_file(file_path, encoding)
        
        def text_to_words_generator():
            for chunk in read_text_by_chunks(file_path, batch_size * 10, encoding):
                # Разбиваем чанк на слова
                words = chunk.split()
                yield words
        
        return analyzer.calculate_layout_comfort_stream(text_to_words_generator(), total_words)
    
    else:
        raise ValueError("file_type должен быть 'words' или 'text'")


def create_comfort_based_rules(layout_config: Dict[str, Any]) -> Dict[str, List]:
    """
    Создает правила на основе удобности раскладки
    """
    analyzer = LayoutAnalyzer(layout_config)
    return analyzer.generate_comfort_rules()


# Пример использования
if __name__ == "__main__":
    # Загрузка раскладки
    layout_config = load_layout_from_json("/Users/evgenii/Develop/py_proj/tr/KVA/example_layouts/qwerty.json")
    
    # Пример 1: Анализ файла со списком слов
    print("Анализ файла со списком слов:")
    result1 = analyze_layout_comfort_from_file(
        layout_config, 
        "/Users/evgenii/Develop/py_proj/tr/KVA/1grams-3.txt", 
        file_type='words',
        batch_size=1000
    )
    print(f"Удобность: {result1['comfort_score']:.2f}")
    
    # Пример 2: Анализ текстового файла (романа)
    # print("\nАнализ текстового файла:")
    # result2 = analyze_layout_comfort_from_file(
    #     layout_config,
    #     "novel.txt",
    #     file_type='text', 
    #     batch_size=2000
    # )
    # print(f"Удобность: {result2['comfort_score']:.2f}")
    # print(f"Проанализировано слов: {result2['total_words']}")
    # print(f"Пар символов: {result2['total_character_pairs']}")