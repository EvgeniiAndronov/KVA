from typing import Dict, List, Tuple, Set, Any, Generator
import json
from collections import defaultdict, Counter
import math
import os
from tqdm import tqdm

class LayoutAnalyzer:
    def __init__(self, layout_config: Dict[str, Any]):
        """
        Инициализация анализатора раскладки
        """
        self.layout_data = layout_config.get("layout", {})
        self.hand_map = {}
        self.position_map = {}
        self.finger_map = {}
        
        self._parse_layout()
    
    def _parse_layout(self):
        """Парсит конфигурацию раскладки и создает маппинги"""
        for letter, data in self.layout_data.items():
            if len(data) >= 3:
                hand, row, col = data[0], data[1], data[2]
                self.hand_map[letter] = hand
                self.position_map[letter] = (hand, row, col)
                finger = self._get_finger_for_column(hand, col)
                self.finger_map[letter] = finger
    
    def _get_finger_for_column(self, hand: str, column: int) -> str:
        """Определяет палец для столбца"""
        if column <= 2:
            return f"{hand}y"
        elif column <= 4:
            return f"{hand}s"
        elif column <= 6:
            return f"{hand}b"
        else:
            return f"{hand}m"
    
    def analyze_word_sequences(self, word: str) -> Dict[str, Any]:
        """
        Анализирует последовательности в слове (совместимость со старым форматом)
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

    def analyze_sequences_all_lengths(self, word: str) -> Dict[str, Any]:
        """
        Анализирует последовательности длиной 2, 3, 4, 5 символов
        """
        result = {
            'word': word,
            'length_2': {'total': 0, 'comfortable': 0, 'uncomfortable': 0, 'partial': 0, 'sequences': []},
            'length_3': {'total': 0, 'comfortable': 0, 'uncomfortable': 0, 'partial': 0, 'sequences': []},
            'length_4': {'total': 0, 'comfortable': 0, 'uncomfortable': 0, 'partial': 0, 'sequences': []},
            'length_5': {'total': 0, 'comfortable': 0, 'uncomfortable': 0, 'partial': 0, 'sequences': []},
            'by_hand': {
                'left': {'total': 0, 'comfortable': 0, 'uncomfortable': 0, 'partial': 0},
                'right': {'total': 0, 'comfortable': 0, 'uncomfortable': 0, 'partial': 0},
                'both': {'total': 0, 'comfortable': 0, 'uncomfortable': 0, 'partial': 0}
            }
        }
        
        for seq_len in [2, 3, 4, 5]:
            if len(word) >= seq_len:
                for i in range(len(word) - seq_len + 1):
                    sequence = word[i:i + seq_len]
                    analysis = self._analyze_sequence_detailed(sequence, seq_len)
                    
                    if analysis:
                        key = f'length_{seq_len}'
                        result[key]['total'] += 1
                        result[key]['sequences'].append(analysis)
                        
                        if analysis['comfort_level'] == 'comfortable':
                            result[key]['comfortable'] += 1
                        elif analysis['comfort_level'] == 'uncomfortable':
                            result[key]['uncomfortable'] += 1
                        else:
                            result[key]['partial'] += 1
                        
                        hand_type = analysis['hand_type']
                        result['by_hand'][hand_type]['total'] += 1
                        if analysis['comfort_level'] == 'comfortable':
                            result['by_hand'][hand_type]['comfortable'] += 1
                        elif analysis['comfort_level'] == 'uncomfortable':
                            result['by_hand'][hand_type]['uncomfortable'] += 1
                        else:
                            result['by_hand'][hand_type]['partial'] += 1
        
        return result
    
    def _analyze_sequence_detailed(self, sequence: str, length: int) -> Dict[str, Any]:
        """
        Детальный анализ последовательности
        """
        if not all(char in self.position_map for char in sequence):
            return None
        
        hands = [self.hand_map[char] for char in sequence]
        unique_hands = set(hands)
        
        if len(unique_hands) == 1:
            hand_type = 'left' if list(unique_hands)[0] == 'l' else 'right'
        else:
            hand_type = 'both'
        
        comfort_level = self._evaluate_sequence_comfort(sequence, hand_type)
        patterns = self._analyze_sequence_patterns(sequence)
        
        return {
            'sequence': sequence,
            'length': length,
            'hand_type': hand_type,
            'comfort_level': comfort_level,
            'patterns': patterns,
            'hands': hands,
            'fingers': [self.finger_map[char] for char in sequence]
        }
    
    def _evaluate_sequence_comfort(self, sequence: str, hand_type: str) -> str:
        """
        Оценивает удобство последовательности
        """
        if len(sequence) < 2:
            return 'unknown'
        
        if hand_type == 'both':
            return 'comfortable'
        
        same_finger_count = 0
        direction_changes = 0
        last_direction = None
        
        for i in range(len(sequence) - 1):
            char1, char2 = sequence[i], sequence[i+1]
            
            if self.finger_map[char1] == self.finger_map[char2]:
                same_finger_count += 1
            
            hand1, row1, col1 = self.position_map[char1]
            hand2, row2, col2 = self.position_map[char2]
            
            row_dir = 1 if row2 > row1 else (-1 if row2 < row1 else 0)
            col_dir = 1 if col2 > col1 else (-1 if col2 < col1 else 0)
            current_direction = (row_dir, col_dir)
            
            if last_direction and current_direction != last_direction:
                direction_changes += 1
            
            last_direction = current_direction
        
        if same_finger_count > len(sequence) * 0.5:
            return 'uncomfortable'
        elif direction_changes > len(sequence) * 0.3:
            return 'partial'
        else:
            return 'comfortable'
    
    def _analyze_sequence_patterns(self, sequence: str) -> Dict[str, Any]:
        """
        Анализирует паттерны в последовательности
        """
        patterns = {
            'hand_changes': 0,
            'finger_changes': 0,
            'row_changes': 0,
            'col_changes': 0,
            'same_finger_streak': 0
        }
        
        current_finger_streak = 1
        max_finger_streak = 1
        
        for i in range(len(sequence) - 1):
            char1, char2 = sequence[i], sequence[i+1]
            
            if self.hand_map[char1] != self.hand_map[char2]:
                patterns['hand_changes'] += 1
            
            if self.finger_map[char1] != self.finger_map[char2]:
                patterns['finger_changes'] += 1
                current_finger_streak = 1
            else:
                current_finger_streak += 1
                max_finger_streak = max(max_finger_streak, current_finger_streak)
            
            hand1, row1, col1 = self.position_map[char1]
            hand2, row2, col2 = self.position_map[char2]
            
            if row1 != row2:
                patterns['row_changes'] += 1
            if col1 != col2:
                patterns['col_changes'] += 1
        
        patterns['max_finger_streak'] = max_finger_streak
        return patterns

    def calculate_layout_comfort(self, wordlist: List[str]) -> Dict[str, Any]:
        """
        Рассчитывает общую удобность раскладки для списка слов (совместимость)
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
            
            for seq_analysis in analysis['sequence_analysis']:
                sequence_types[seq_analysis['type']] += 1
        
        total_analyzed_pairs = total_sequences
        
        if total_analyzed_pairs > 0:
            hand_change_percent = (total_hand_changes / total_analyzed_pairs) * 100
            direction_change_percent = (total_direction_changes / total_analyzed_pairs) * 100
            same_hand_percent = (total_same_hand / total_analyzed_pairs) * 100
            same_finger_percent = (total_same_finger / total_analyzed_pairs) * 100
        else:
            hand_change_percent = direction_change_percent = same_hand_percent = same_finger_percent = 0
        
        comfort_score = (
            hand_change_percent * 1.0 +
            same_hand_percent * 0.3 +
            -same_finger_percent * 0.5
        )
        
        return {
            'total_errors': 0,  # Для совместимости
            'total_words': len(wordlist),
            'total_characters': sum(len(word) for word in wordlist),
            'processed_characters': sum(len(word) for word in wordlist),
            'unknown_characters': set(),
            'finger_statistics': {},
            'finger_errors': {},
            'finger_detailed_data': {},
            'layout_name': 'unknown',
            'avg_errors_per_word': 0,
            'avg_errors_per_char': 0,
            # Новые данные для графиков
            'comfort_score': comfort_score,
            'total_sequences': total_sequences,
            'sequence_statistics': {
                'hand_changes': total_hand_changes,
                'direction_changes': total_direction_changes,
                'same_hand_sequences': total_same_hand,
                'same_finger_sequences': total_same_finger,
                'hand_change_percent': hand_change_percent,
                'direction_change_percent': direction_change_percent,
                'same_hand_percent': same_hand_percent,
                'same_finger_percent': same_finger_percent
            },
            'sequence_type_distribution': dict(sequence_types),
            'word_analyses': word_analyses
        }

    def calculate_layout_comfort_stream(self, wordlist_generator: Generator[List[str], None, None], 
                                      total_words: int = None) -> Dict[str, Any]:
        """
        Рассчитывает удобность раскладки для потокового генератора слов
        """
        total_sequences = 0
        total_hand_changes = 0
        total_direction_changes = 0
        total_same_hand = 0
        total_same_finger = 0
        processed_words = 0
        total_characters = 0
        
        sequence_types = Counter()
        
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
                batch_chars = 0
                
                for word in batch:
                    analysis = self.analyze_word_sequences(word)
                    
                    batch_sequences += analysis['total_sequences']
                    batch_hand_changes += analysis['hand_changes']
                    batch_direction_changes += analysis['direction_changes']
                    batch_same_hand += analysis['same_hand_sequences']
                    batch_same_finger += analysis['same_finger_sequences']
                    batch_chars += len(word)
                    
                    for seq_analysis in analysis['sequence_analysis']:
                        sequence_types[seq_analysis['type']] += 1
                
                total_sequences += batch_sequences
                total_hand_changes += batch_hand_changes
                total_direction_changes += batch_direction_changes
                total_same_hand += batch_same_hand
                total_same_finger += batch_same_finger
                total_characters += batch_chars
                processed_words += len(batch)
                
                pbar.update(len(batch))
                pbar.set_postfix({
                    'слов': processed_words,
                    'пар_символов': total_sequences
                })
        
        finally:
            pbar.close()
        
        total_analyzed_pairs = total_sequences
        
        if total_analyzed_pairs > 0:
            hand_change_percent = (total_hand_changes / total_analyzed_pairs) * 100
            direction_change_percent = (total_direction_changes / total_analyzed_pairs) * 100
            same_hand_percent = (total_same_hand / total_analyzed_pairs) * 100
            same_finger_percent = (total_same_finger / total_analyzed_pairs) * 100
        else:
            hand_change_percent = direction_change_percent = same_hand_percent = same_finger_percent = 0
        
        comfort_score = (
            hand_change_percent * 1.0 +
            same_hand_percent * 0.3 +
            -same_finger_percent * 0.5
        )
        
        return {
            'total_errors': 0,
            'total_words': processed_words,
            'total_characters': total_characters,
            'processed_characters': total_characters,
            'unknown_characters': set(),
            'finger_statistics': {},
            'finger_errors': {},
            'finger_detailed_data': {},
            'layout_name': 'unknown',
            'avg_errors_per_word': 0,
            'avg_errors_per_char': 0,
            # Новые данные
            'comfort_score': comfort_score,
            'total_sequences': total_sequences,
            'sequence_statistics': {
                'hand_changes': total_hand_changes,
                'direction_changes': total_direction_changes,
                'same_hand_sequences': total_same_hand,
                'same_finger_sequences': total_same_finger,
                'hand_change_percent': hand_change_percent,
                'direction_change_percent': direction_change_percent,
                'same_hand_percent': same_hand_percent,
                'same_finger_percent': same_finger_percent
            },
            'sequence_type_distribution': dict(sequence_types)
        }

    def calculate_comprehensive_comfort(self, wordlist: List[str]) -> Dict[str, Any]:
        """
        Комплексный анализ для всех длин последовательностей (для графиков)
        """
        total_stats = {
            'length_2': {'total': 0, 'comfortable': 0, 'uncomfortable': 0, 'partial': 0},
            'length_3': {'total': 0, 'comfortable': 0, 'uncomfortable': 0, 'partial': 0},
            'length_4': {'total': 0, 'comfortable': 0, 'uncomfortable': 0, 'partial': 0},
            'length_5': {'total': 0, 'comfortable': 0, 'uncomfortable': 0, 'partial': 0},
            'by_hand': {
                'left': {'total': 0, 'comfortable': 0, 'uncomfortable': 0, 'partial': 0},
                'right': {'total': 0, 'comfortable': 0, 'uncomfortable': 0, 'partial': 0},
                'both': {'total': 0, 'comfortable': 0, 'uncomfortable': 0, 'partial': 0}
            },
            'word_stats': {
                'total_words': len(wordlist),
                'words_with_sequences': 0,
                'avg_sequences_per_word': 0
            },
            'sequence_examples': {
                'comfortable': [],
                'uncomfortable': [],
                'partial': []
            }
        }
        
        total_sequences_all = 0
        
        for word in tqdm(wordlist, desc="Анализ последовательностей"):
            analysis = self.analyze_sequences_all_lengths(word)
            has_sequences = False
            
            for length in [2, 3, 4, 5]:
                key = f'length_{length}'
                length_data = analysis[key]
                
                total_stats[key]['total'] += length_data['total']
                total_stats[key]['comfortable'] += length_data['comfortable']
                total_stats[key]['uncomfortable'] += length_data['uncomfortable']
                total_stats[key]['partial'] += length_data['partial']
                
                total_sequences_all += length_data['total']
                if length_data['total'] > 0:
                    has_sequences = True
                
                for seq_analysis in length_data['sequences']:
                    if len(total_stats['sequence_examples'][seq_analysis['comfort_level']]) < 10:
                        total_stats['sequence_examples'][seq_analysis['comfort_level']].append({
                            'sequence': seq_analysis['sequence'],
                            'length': seq_analysis['length'],
                            'hand_type': seq_analysis['hand_type'],
                            'comfort_level': seq_analysis['comfort_level']
                        })
            
            for hand_type in ['left', 'right', 'both']:
                hand_data = analysis['by_hand'][hand_type]
                total_stats['by_hand'][hand_type]['total'] += hand_data['total']
                total_stats['by_hand'][hand_type]['comfortable'] += hand_data['comfortable']
                total_stats['by_hand'][hand_type]['uncomfortable'] += hand_data['uncomfortable']
                total_stats['by_hand'][hand_type]['partial'] += hand_data['partial']
            
            if has_sequences:
                total_stats['word_stats']['words_with_sequences'] += 1
        
        # Рассчитываем проценты
        for length in [2, 3, 4, 5]:
            key = f'length_{length}'
            total = total_stats[key]['total']
            if total > 0:
                total_stats[key]['comfortable_percent'] = (total_stats[key]['comfortable'] / total) * 100
                total_stats[key]['uncomfortable_percent'] = (total_stats[key]['uncomfortable'] / total) * 100
                total_stats[key]['partial_percent'] = (total_stats[key]['partial'] / total) * 100
            else:
                total_stats[key]['comfortable_percent'] = 0
                total_stats[key]['uncomfortable_percent'] = 0
                total_stats[key]['partial_percent'] = 0
        
        for hand_type in ['left', 'right', 'both']:
            total = total_stats['by_hand'][hand_type]['total']
            if total > 0:
                total_stats['by_hand'][hand_type]['comfortable_percent'] = (
                    total_stats['by_hand'][hand_type]['comfortable'] / total) * 100
                total_stats['by_hand'][hand_type]['uncomfortable_percent'] = (
                    total_stats['by_hand'][hand_type]['uncomfortable'] / total) * 100
                total_stats['by_hand'][hand_type]['partial_percent'] = (
                    total_stats['by_hand'][hand_type]['partial'] / total) * 100
            else:
                total_stats['by_hand'][hand_type]['comfortable_percent'] = 0
                total_stats['by_hand'][hand_type]['uncomfortable_percent'] = 0
                total_stats['by_hand'][hand_type]['partial_percent'] = 0
        
        total_stats['word_stats']['avg_sequences_per_word'] = (
            total_sequences_all / len(wordlist) if wordlist else 0
        )
        
        return total_stats

    def prepare_data_for_plots(self, comfort_stats: Dict[str, Any]) -> Dict[str, Any]:
        """
        Подготавливает данные для построения графиков
        """
        plot_data = {
            'sequence_lengths': {
                'lengths': ['2 символа', '3 символа', '4 символа', '5 символов'],
                'comfortable': [],
                'uncomfortable': [],
                'partial': [],
                'total_sequences': []
            },
            'by_hand': {
                'hands': ['Левая рука', 'Правая рука', 'Обе руки'],
                'comfortable': [],
                'uncomfortable': [],
                'partial': [],
                'total_sequences': []
            },
            'percentages': {
                'by_length': {},
                'by_hand': {},
                'overall': {}
            }
        }
        
        for length in [2, 3, 4, 5]:
            key = f'length_{length}'
            plot_data['sequence_lengths']['comfortable'].append(
                comfort_stats[key].get('comfortable_percent', 0)
            )
            plot_data['sequence_lengths']['uncomfortable'].append(
                comfort_stats[key].get('uncomfortable_percent', 0)
            )
            plot_data['sequence_lengths']['partial'].append(
                comfort_stats[key].get('partial_percent', 0)
            )
            plot_data['sequence_lengths']['total_sequences'].append(
                comfort_stats[key]['total']
            )
            
            plot_data['percentages']['by_length'][f'{length}_symbols'] = {
                'comfortable': comfort_stats[key].get('comfortable_percent', 0),
                'uncomfortable': comfort_stats[key].get('uncomfortable_percent', 0),
                'partial': comfort_stats[key].get('partial_percent', 0),
                'total': comfort_stats[key]['total']
            }
        
        for hand_type, hand_label in [('left', 'Левая рука'), ('right', 'Правая рука'), ('both', 'Обе руки')]:
            plot_data['by_hand']['comfortable'].append(
                comfort_stats['by_hand'][hand_type].get('comfortable_percent', 0)
            )
            plot_data['by_hand']['uncomfortable'].append(
                comfort_stats['by_hand'][hand_type].get('uncomfortable_percent', 0)
            )
            plot_data['by_hand']['partial'].append(
                comfort_stats['by_hand'][hand_type].get('partial_percent', 0)
            )
            plot_data['by_hand']['total_sequences'].append(
                comfort_stats['by_hand'][hand_type]['total']
            )
            
            plot_data['percentages']['by_hand'][hand_label] = {
                'comfortable': comfort_stats['by_hand'][hand_type].get('comfortable_percent', 0),
                'uncomfortable': comfort_stats['by_hand'][hand_type].get('uncomfortable_percent', 0),
                'partial': comfort_stats['by_hand'][hand_type].get('partial_percent', 0),
                'total': comfort_stats['by_hand'][hand_type]['total']
            }
        
        total_comfortable = sum(comfort_stats[f'length_{length}']['comfortable'] for length in [2, 3, 4, 5])
        total_uncomfortable = sum(comfort_stats[f'length_{length}']['uncomfortable'] for length in [2, 3, 4, 5])
        total_partial = sum(comfort_stats[f'length_{length}']['partial'] for length in [2, 3, 4, 5])
        total_all = total_comfortable + total_uncomfortable + total_partial
        
        if total_all > 0:
            plot_data['percentages']['overall'] = {
                'comfortable': (total_comfortable / total_all) * 100,
                'uncomfortable': (total_uncomfortable / total_all) * 100,
                'partial': (total_partial / total_all) * 100,
                'total_sequences': total_all
            }
        else:
            plot_data['percentages']['overall'] = {
                'comfortable': 0, 'uncomfortable': 0, 'partial': 0, 'total_sequences': 0
            }
        
        plot_data['examples'] = comfort_stats.get('sequence_examples', {})
        plot_data['word_stats'] = comfort_stats.get('word_stats', {})
        
        return plot_data


# Функции для работы с файлами
def load_layout_from_json(file_path: str) -> Dict[str, Any]:
    """Загружает конфигурацию раскладки из JSON файла"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def read_words_by_lines(file_path: str, batch_size: int = 1000, 
                       encoding: str = 'utf-8') -> Generator[List[str], None, None]:
    """Читает файл построчно, возвращая батчи слов"""
    current_batch = []
    
    with open(file_path, 'r', encoding=encoding) as f:
        for line in f:
            line = line.strip()
            if line:
                words = line.split()
                current_batch.extend(words)
                
                if len(current_batch) >= batch_size:
                    yield current_batch
                    current_batch = []
    
    if current_batch:
        yield current_batch

def count_lines_in_file(file_path: str, encoding: str = 'utf-8') -> int:
    """Считает количество строк в файле"""
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            return sum(1 for _ in f)
    except:
        return 0

def analyze_layout_comfort_from_file(layout_config: Dict[str, Any], 
                                   file_path: str, 
                                   file_type: str = 'words',
                                   batch_size: int = 1000,
                                   encoding: str = 'utf-8',
                                   max_samples_for_plots: int = 10000) -> Dict[str, Any]:
    """
    Анализирует удобность раскладки из файла с ВСЕГДА доступными данными для графиков
    """
    analyzer = LayoutAnalyzer(layout_config)
    
    if file_type == 'words':
        total_words = count_lines_in_file(file_path, encoding)
        
        # Собираем слова для анализа графиков
        plot_words = []
        word_generator = read_words_by_lines(file_path, batch_size, encoding)
        
        # Промежуточные переменные для статистики
        total_sequences = 0
        total_hand_changes = 0
        total_direction_changes = 0
        total_same_hand = 0
        total_same_finger = 0
        processed_words = 0
        total_characters = 0
        sequence_types = Counter()
        
        if total_words:
            pbar = tqdm(total=total_words, desc="Анализ удобности")
        else:
            pbar = tqdm(desc="Анализ удобности")
        
        try:
            for batch in word_generator:
                batch_sequences = 0
                batch_hand_changes = 0
                batch_direction_changes = 0
                batch_same_hand = 0
                batch_same_finger = 0
                batch_chars = 0
                
                for word in batch:
                    # Собираем слова для графиков (до максимального количества)
                    if len(plot_words) < max_samples_for_plots:
                        plot_words.append(word)
                    
                    # Анализируем последовательности
                    analysis = analyzer.analyze_word_sequences(word)
                    
                    batch_sequences += analysis['total_sequences']
                    batch_hand_changes += analysis['hand_changes']
                    batch_direction_changes += analysis['direction_changes']
                    batch_same_hand += analysis['same_hand_sequences']
                    batch_same_finger += analysis['same_finger_sequences']
                    batch_chars += len(word)
                    
                    for seq_analysis in analysis['sequence_analysis']:
                        sequence_types[seq_analysis['type']] += 1
                
                total_sequences += batch_sequences
                total_hand_changes += batch_hand_changes
                total_direction_changes += batch_direction_changes
                total_same_hand += batch_same_hand
                total_same_finger += batch_same_finger
                total_characters += batch_chars
                processed_words += len(batch)
                
                pbar.update(len(batch))
                pbar.set_postfix({
                    'слов': processed_words,
                    'пар_символов': total_sequences
                })
        
        finally:
            pbar.close()
        
        # Рассчитываем основную статистику
        total_analyzed_pairs = total_sequences
        
        if total_analyzed_pairs > 0:
            hand_change_percent = (total_hand_changes / total_analyzed_pairs) * 100
            direction_change_percent = (total_direction_changes / total_analyzed_pairs) * 100
            same_hand_percent = (total_same_hand / total_analyzed_pairs) * 100
            same_finger_percent = (total_same_finger / total_analyzed_pairs) * 100
        else:
            hand_change_percent = direction_change_percent = same_hand_percent = same_finger_percent = 0
        
        comfort_score = (
            hand_change_percent * 1.0 +
            same_hand_percent * 0.3 +
            -same_finger_percent * 0.5
        )
        
        # Базовый результат
        result = {
            'total_errors': 0,
            'total_words': processed_words,
            'total_characters': total_characters,
            'processed_characters': total_characters,
            'unknown_characters': set(),
            'finger_statistics': {},
            'finger_errors': {},
            'finger_detailed_data': {},
            'layout_name': 'unknown',
            'avg_errors_per_word': 0,
            'avg_errors_per_char': 0,
            'comfort_score': comfort_score,
            'total_sequences': total_sequences,
            'sequence_statistics': {
                'hand_changes': total_hand_changes,
                'direction_changes': total_direction_changes,
                'same_hand_sequences': total_same_hand,
                'same_finger_sequences': total_same_finger,
                'hand_change_percent': hand_change_percent,
                'direction_change_percent': direction_change_percent,
                'same_hand_percent': same_hand_percent,
                'same_finger_percent': same_finger_percent
            },
            'sequence_type_distribution': dict(sequence_types)
        }
        
        # ВСЕГДА добавляем данные для графиков
        if plot_words:
            comprehensive_stats = analyzer.calculate_comprehensive_comfort(plot_words)
            plot_data = analyzer.prepare_data_for_plots(comprehensive_stats)
            
            # Добавляем информацию о выборке
            plot_data['sample_info'] = {
                'sample_size': len(plot_words),
                'total_words': processed_words,
                'is_full_sample': len(plot_words) == processed_words
            }
            
            result['plot_data'] = plot_data
            result['comprehensive_stats'] = comprehensive_stats
        else:
            # Если файл пустой
            result['plot_data'] = create_empty_plot_data()
            result['comprehensive_stats'] = create_empty_comprehensive_stats()
        
        return result
    
    else:
        raise ValueError("Поддерживается только file_type='words'")

def create_empty_plot_data() -> Dict[str, Any]:
    """Создает пустую структуру данных для графиков"""
    return {
        'sequence_lengths': {
            'lengths': ['2 символа', '3 символа', '4 символа', '5 символов'],
            'comfortable': [0, 0, 0, 0],
            'uncomfortable': [0, 0, 0, 0],
            'partial': [0, 0, 0, 0],
            'total_sequences': [0, 0, 0, 0]
        },
        'by_hand': {
            'hands': ['Левая рука', 'Правая рука', 'Обе руки'],
            'comfortable': [0, 0, 0],
            'uncomfortable': [0, 0, 0],
            'partial': [0, 0, 0],
            'total_sequences': [0, 0, 0]
        },
        'percentages': {
            'by_length': {
                '2_symbols': {'comfortable': 0, 'uncomfortable': 0, 'partial': 0, 'total': 0},
                '3_symbols': {'comfortable': 0, 'uncomfortable': 0, 'partial': 0, 'total': 0},
                '4_symbols': {'comfortable': 0, 'uncomfortable': 0, 'partial': 0, 'total': 0},
                '5_symbols': {'comfortable': 0, 'uncomfortable': 0, 'partial': 0, 'total': 0}
            },
            'by_hand': {
                'Левая рука': {'comfortable': 0, 'uncomfortable': 0, 'partial': 0, 'total': 0},
                'Правая рука': {'comfortable': 0, 'uncomfortable': 0, 'partial': 0, 'total': 0},
                'Обе руки': {'comfortable': 0, 'uncomfortable': 0, 'partial': 0, 'total': 0}
            },
            'overall': {'comfortable': 0, 'uncomfortable': 0, 'partial': 0, 'total_sequences': 0}
        },
        'examples': {
            'comfortable': [],
            'uncomfortable': [],
            'partial': []
        },
        'word_stats': {
            'total_words': 0,
            'words_with_sequences': 0,
            'avg_sequences_per_word': 0
        },
        'sample_info': {
            'sample_size': 0,
            'total_words': 0,
            'is_full_sample': True
        }
    }

def create_empty_comprehensive_stats() -> Dict[str, Any]:
    """Создает пустую структуру комплексной статистики"""
    return {
        'length_2': {'total': 0, 'comfortable': 0, 'uncomfortable': 0, 'partial': 0},
        'length_3': {'total': 0, 'comfortable': 0, 'uncomfortable': 0, 'partial': 0},
        'length_4': {'total': 0, 'comfortable': 0, 'uncomfortable': 0, 'partial': 0},
        'length_5': {'total': 0, 'comfortable': 0, 'uncomfortable': 0, 'partial': 0},
        'by_hand': {
            'left': {'total': 0, 'comfortable': 0, 'uncomfortable': 0, 'partial': 0},
            'right': {'total': 0, 'comfortable': 0, 'uncomfortable': 0, 'partial': 0},
            'both': {'total': 0, 'comfortable': 0, 'uncomfortable': 0, 'partial': 0}
        },
        'word_stats': {
            'total_words': 0,
            'words_with_sequences': 0,
            'avg_sequences_per_word': 0
        },
        'sequence_examples': {
            'comfortable': [],
            'uncomfortable': [],
            'partial': []
        }
    }

def print_comprehensive_analysis(result):
    """
    Выводит все данные анализа с подробными комментариями
    """
    print("=" * 80)
    print("КОМПЛЕКСНЫЙ АНАЛИЗ РАСКЛАДКИ")
    print("=" * 80)
    
    # Основные метрики
    print("\n📊 ОСНОВНЫЕ МЕТРИКИ:")
    print(f"  • Общая оценка удобности: {result['comfort_score']:.2f}")
    print(f"  • Всего слов проанализировано: {result['total_words']:,}")
    print(f"  • Всего символов: {result['total_characters']:,}")
    print(f"  • Всего последовательностей (2 символа): {result['total_sequences']:,}")
    
    # Статистика по последовательностям из 2 символов
    seq_stats = result['sequence_statistics']
    print(f"\n🔄 СТАТИСТИКА ПОСЛЕДОВАТЕЛЬНОСТЕЙ (2 СИМВОЛА):")
    print(f"  • Смена рук: {seq_stats['hand_changes']:,} ({seq_stats['hand_change_percent']:.1f}%) - ⭐ УДОБНО")
    print(f"  • Одна рука: {seq_stats['same_hand_sequences']:,} ({seq_stats['same_hand_percent']:.1f}%) - ✅ НОРМАЛЬНО")
    print(f"  • Один палец: {seq_stats['same_finger_sequences']:,} ({seq_stats['same_finger_percent']:.1f}%) - ❌ НЕУДОБНО")
    print(f"  • Смена направления: {seq_stats['direction_changes']:,} ({seq_stats['direction_change_percent']:.1f}%) - 🔄 ЧАСТИЧНО УДОБНО")
    
    # Распределение типов последовательностей
    print(f"\n📈 РАСПРЕДЕЛЕНИЕ ТИПОВ ПОСЛЕДОВАТЕЛЬНОСТЕЙ:")
    for seq_type, count in result['sequence_type_distribution'].items():
        percent = (count / result['total_sequences'] * 100) if result['total_sequences'] > 0 else 0
        type_desc = {
            'hand_change': 'Смена руки ⭐',
            'same_direction': 'Одно направление ✅', 
            'direction_change': 'Смена направления 🔄',
            'same_finger': 'Один палец ❌'
        }.get(seq_type, seq_type)
        print(f"  • {type_desc}: {count:,} ({percent:.1f}%)")
    
    # Данные для графиков
    if 'plot_data' in result:
        plot_data = result['plot_data']
        sample_info = plot_data.get('sample_info', {})
        
        print(f"\n🎯 ДАННЫЕ ДЛЯ ГРАФИКОВ (на основе {sample_info.get('sample_size', 0):,} слов):")
        
        # Последовательности по длинам
        print(f"\n📏 ГИСТОГРАММЫ ПО ДЛИНАМ ПОСЛЕДОВАТЕЛЬНОСТЕЙ:")
        lengths = plot_data['sequence_lengths']['lengths']
        comfortable = plot_data['sequence_lengths']['comfortable']
        uncomfortable = plot_data['sequence_lengths']['uncomfortable']
        partial = plot_data['sequence_lengths']['partial']
        totals = plot_data['sequence_lengths']['total_sequences']
        
        for i, length in enumerate(lengths):
            print(f"  • {length}:")
            print(f"      Удобные: {comfortable[i]:.1f}% ({totals[i]:,} последовательностей)")
            print(f"      Неудобные: {uncomfortable[i]:.1f}%")
            print(f"      Частично удобные: {partial[i]:.1f}%")
        
        # Последовательности по рукам
        print(f"\n👐 ГИСТОГРАММЫ ПО РУКАМ:")
        hands = plot_data['by_hand']['hands']
        hand_comfortable = plot_data['by_hand']['comfortable']
        hand_uncomfortable = plot_data['by_hand']['uncomfortable']
        hand_partial = plot_data['by_hand']['partial']
        hand_totals = plot_data['by_hand']['total_sequences']
        
        for i, hand in enumerate(hands):
            print(f"  • {hand}:")
            print(f"      Удобные: {hand_comfortable[i]:.1f}% ({hand_totals[i]:,} последовательностей)")
            print(f"      Неудобные: {hand_uncomfortable[i]:.1f}%")
            print(f"      Частично удобные: {hand_partial[i]:.1f}%")
        
        # Процентные соотношения
        print(f"\n📊 ПРОЦЕНТНЫЕ СООТНОШЕНИЯ:")
        
        # По длинам
        print(f"  ПО ДЛИНАМ ПОСЛЕДОВАТЕЛЬНОСТЕЙ:")
        for length_key, data in plot_data['percentages']['by_length'].items():
            length_name = length_key.replace('_', ' ')
            print(f"    • {length_name}: удобно {data['comfortable']:.1f}%, неудобно {data['uncomfortable']:.1f}%, частично {data['partial']:.1f}%")
        
        # По рукам
        print(f"  ПО РУКАМ:")
        for hand_key, data in plot_data['percentages']['by_hand'].items():
            print(f"    • {hand_key}: удобно {data['comfortable']:.1f}%, неудобно {data['uncomfortable']:.1f}%, частично {data['partial']:.1f}%")
        
        # Общие проценты
        overall = plot_data['percentages']['overall']
        print(f"  ОБЩИЕ:")
        print(f"    • Удобные: {overall['comfortable']:.1f}%")
        print(f"    • Неудобные: {overall['uncomfortable']:.1f}%")
        print(f"    • Частично удобные: {overall['partial']:.1f}%")
        print(f"    • Всего последовательностей: {overall['total_sequences']:,}")
        
        # Примеры последовательностей
        print(f"\n🔍 ПРИМЕРЫ ПОСЛЕДОВАТЕЛЬНОСТЕЙ:")
        examples = plot_data.get('examples', {})
        for comfort_type in ['comfortable', 'uncomfortable', 'partial']:
            type_desc = {
                'comfortable': 'Удобные ⭐',
                'uncomfortable': 'Неудобные ❌', 
                'partial': 'Частично удобные 🔄'
            }[comfort_type]
            
            seq_examples = examples.get(comfort_type, [])
            if seq_examples:
                print(f"  • {type_desc}:")
                for example in seq_examples[:5]:  # Показываем первые 5 примеров
                    hand_desc = {
                        'left': 'левая рука',
                        'right': 'правая рука', 
                        'both': 'обе руки'
                    }.get(example['hand_type'], example['hand_type'])
                    print(f"      '{example['sequence']}' ({example['length']} символа, {hand_desc})")
        
        # Статистика по словам
        word_stats = plot_data.get('word_stats', {})
        print(f"\n📝 СТАТИСТИКА ПО СЛОВАМ:")
        print(f"  • Всего слов в выборке: {word_stats.get('total_words', 0):,}")
        print(f"  • Слов с последовательностями: {word_stats.get('words_with_sequences', 0):,}")
        print(f"  • Среднее последовательностей на слово: {word_stats.get('avg_sequences_per_word', 0):.2f}")
        
        # Информация о выборке
        if sample_info:
            print(f"\n📋 ИНФОРМАЦИЯ О ВЫБОРКЕ:")
            print(f"  • Размер выборки для анализа: {sample_info.get('sample_size', 0):,} слов")
            print(f"  • Всего слов в файле: {sample_info.get('total_words', 0):,}")
            print(f"  • Полная выборка: {'Да' if sample_info.get('is_full_sample', False) else 'Нет'}")
    
    else:
        print(f"\n❌ ДАННЫЕ ДЛЯ ГРАФИКОВ НЕДОСТУПНЫ")
    
    print("\n" + "=" * 80)
    print("АНАЛИЗ ЗАВЕРШЕН")
    print("=" * 80)

# Использование:
if __name__ == "__main__":
    # Загрузка раскладки
    layout_config = load_layout_from_json("/Users/evgenii/Develop/py_proj/tr/KVA/example_layouts/qwerty.json")
    
    # Анализ файла
    print("Анализ файла со списком слов:")
    result1 = analyze_layout_comfort_from_file(
        layout_config, 
        "/Users/evgenii/Develop/py_proj/tr/KVA/1grams-3.txt", 
        file_type='words',
        batch_size=1000
    )
    
    # Выводим ВСЕ данные
    print_comprehensive_analysis(result1)

# Пример использования (совместим с вашим форматом)
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
    print(f"Всего слов: {result1['total_words']}")
    print(f"Всего последовательностей: {result1['total_sequences']}")
    print(f"Смена рук: {result1['sequence_statistics']['hand_change_percent']:.1f}%")
    
    # Если есть данные для графиков
    if 'plot_data' in result1:
        print(f"\nДанные для графиков доступны!")
        print_comprehensive_analysis(result1)