from typing import Dict, List, Tuple, Set, Any, Generator, Optional, Union
import json
from collections import defaultdict, Counter
import math
import os
from tqdm import tqdm

class LayoutAnalyzer:
    def __init__(self, layout_config: Dict[str, Any], layout_name: str = ""):
        """
        Инициализация анализатора раскладки с учетом модификаторов
        """
        self.layout_name = layout_name
        self.layout_data = layout_config.get("layout", {})
        self.hand_map = {}
        self.finger_map = {}
        self.position_map = {}
        self.column_map = {}
        self.row_map = {}
        self.modifiers_map = {}  # Модификаторы для каждого символа
        
        self._parse_layout()
    
    def _parse_layout(self):
        """Парсит конфигурацию раскладки и создает маппинги"""
        for letter, data in self.layout_data.items():
            # Обрабатываем два формата данных: словарь или список
            if isinstance(data, dict):
                # Формат 1: словарь с ключами
                hand = data.get("hand", "").lower()
                finger = data.get("finger", "")
                row = data.get("row", 0)
                column = data.get("column", 0)
                modifiers = data.get("modifiers", [])
            elif isinstance(data, list):
                # Формат 2: список [hand, finger, row, column, ...modifiers]
                if len(data) >= 4:
                    hand = str(data[0]).lower() if data[0] else ""
                    finger = str(data[1]) if len(data) > 1 else ""
                    row = int(data[2]) if len(data) > 2 else 0
                    column = int(data[3]) if len(data) > 3 else 0
                    modifiers = data[4:] if len(data) > 4 else []
                else:
                    continue  # Пропускаем некорректные записи
            else:
                continue  # Пропускаем неизвестный формат
            
            self.hand_map[letter] = hand
            self.finger_map[letter] = finger
            self.position_map[letter] = (hand, finger, row, column)
            self.column_map[letter] = column
            self.row_map[letter] = row
            self.modifiers_map[letter] = modifiers
    
    def get_finger_order(self, finger: str) -> int:
        """
        Возвращает порядковый номер пальца для определения направления
        Мизинец = 1, Безымянный = 2, Средний = 3, Указательный = 4
        """
        finger_mapping = {
            "L1": 1,  # Мизинец левый
            "L2": 2,  # Безымянный левый
            "L3": 3,  # Средний левый
            "L4": 4,  # Указательный левый
            "R1": 4,  # Указательный правый
            "R2": 3,  # Средний правый
            "R3": 2,  # Безымянный правый
            "R4": 1,  # Мизинец правый
        }
        return finger_mapping.get(finger, 0)
    
    def analyze_character_with_modifiers(self, char: str) -> List[Dict[str, Any]]:
        """
        Анализирует символ с учетом модификаторов
        Возвращает список нажатий для символа
        """
        if char not in self.modifiers_map:
            return [{
                'char': char,
                'hand': self.hand_map.get(char, ''),
                'finger': self.finger_map.get(char, ''),
                'is_modifier': False,
                'modifier_type': None
            }]
        
        modifiers = self.modifiers_map[char]
        actions = []
        
        # Обрабатываем модификаторы
        for modifier in modifiers:
            if isinstance(modifier, str) and modifier == "shift":
                # Shift на той же руке, что и символ
                hand = self.hand_map.get(char, '')
                # Для shift обычно используется мизинец той же руки
                shift_finger = "L1" if hand == "left" else "R4"
                actions.append({
                    'char': 'Shift',
                    'hand': hand,
                    'finger': shift_finger,
                    'is_modifier': True,
                    'modifier_type': 'shift'
                })
            elif isinstance(modifier, str) and modifier == "alt":
                # Alt всегда правой рукой (обычно правым большим пальцем или правым мизинцем)
                actions.append({
                    'char': 'Alt',
                    'hand': 'right',
                    'finger': 'R4',  # Правый мизинец для Alt
                    'is_modifier': True,
                    'modifier_type': 'alt'
                })
        
        # Добавляем сам символ
        actions.append({
            'char': char,
            'hand': self.hand_map.get(char, ''),
            'finger': self.finger_map.get(char, ''),
            'is_modifier': False,
            'modifier_type': None
        })
        
        return actions
    
    def analyze_sequence_comfort_with_modifiers(self, sequence: str) -> Dict[str, Any]:
        """
        Анализирует удобство последовательности с учетом модификаторов
        """
        if len(sequence) < 2:
            return {'comfort': 'unknown', 'reason': 'too_short'}
        
        # Для последовательности из одинаковых символов (без учета модификаторов)
        if len(set(sequence)) == 1:
            # Проверяем, есть ли модификаторы
            char = sequence[0]
            actions = self.analyze_character_with_modifiers(char)
            
            # Если есть только один символ без модификаторов или с модификаторами на той же руке
            if len(actions) == 1 or all(a['hand'] == actions[0]['hand'] for a in actions):
                return {
                    'comfort': 'comfortable',
                    'reason': 'same_characters',
                    'hand_type': 'single_hand',
                    'sequence': sequence,
                    'length': len(sequence),
                    'has_modifiers': len(actions) > 1
                }
        
        # Разбираем последовательность на действия (с учетом модификаторов)
        all_actions = []
        for char in sequence:
            if char in self.modifiers_map:  # Проверяем, что символ есть в раскладке
                char_actions = self.analyze_character_with_modifiers(char)
                all_actions.extend(char_actions)
            else:
                # Если символа нет в раскладке, пропускаем
                continue
        
        if not all_actions:
            return {'comfort': 'unknown', 'reason': 'no_valid_chars'}
        
        # Убираем модификаторы для анализа последовательности (они не увеличивают длину)
        # Но учитываем их при определении смены руки
        key_actions = [a for a in all_actions if not a['is_modifier']]
        
        if len(key_actions) < 2:
            return {'comfort': 'unknown', 'reason': 'only_modifiers'}
        
        # Проверяем смену руки с учетом модификаторов
        # Собираем все уникальные руки в последовательности
        all_hands = set()
        for action in all_actions:
            if action['hand']:  # Проверяем, что рука определена
                all_hands.add(action['hand'])
        
        if not all_hands:
            return {'comfort': 'unknown', 'reason': 'no_hand_info'}
        
        if len(all_hands) > 1:
            # Разные руки в последовательности (включая модификаторы)
            return {
                'comfort': 'uncomfortable',
                'reason': 'hand_change_with_modifiers',
                'hand_type': 'both',
                'sequence': sequence,
                'length': len(sequence),
                'has_modifiers': any(a['is_modifier'] for a in all_actions)
            }
        
        # Определяем руку
        hand_type = list(all_hands)[0] if all_hands else 'unknown'
        
        # Для двух символов (без учета модификаторов в длине)
        if len(key_actions) == 2:
            action1, action2 = key_actions[0], key_actions[1]
            
            # Если один и тот же палец - удобно
            if action1['finger'] == action2['finger']:
                return {
                    'comfort': 'comfortable',
                    'reason': 'same_finger',
                    'hand_type': hand_type,
                    'sequence': sequence,
                    'length': len(sequence),
                    'has_modifiers': any(a['is_modifier'] for a in all_actions)
                }
            
            # Получаем порядковые номара пальцев
            order1 = self.get_finger_order(action1['finger'])
            order2 = self.get_finger_order(action2['finger'])
            
            if order1 == 0 or order2 == 0:
                return {'comfort': 'unknown', 'reason': 'unknown_finger'}
            
            if order1 < order2:
                # От мизинца к указательному (внешние → внутренние) - УДОБНО
                return {
                    'comfort': 'comfortable',
                    'reason': 'outside_to_inside',
                    'hand_type': hand_type,
                    'sequence': sequence,
                    'length': len(sequence),
                    'has_modifiers': any(a['is_modifier'] for a in all_actions)
                }
            else:
                # От указательного к мизинцу (внутренние → внешние) - ЧАСТИЧНО УДОБНО
                return {
                    'comfort': 'partial',
                    'reason': 'inside_to_outside',
                    'hand_type': hand_type,
                    'sequence': sequence,
                    'length': len(sequence),
                    'has_modifiers': any(a['is_modifier'] for a in all_actions)
                }
        
        # Для последовательностей из 3+ символов (без учета модификаторов в длине)
        else:
            # Проверяем, все ли пальцы разные
            fingers = [action['finger'] for action in key_actions]
            if len(set(fingers)) == 1:
                # Один и тот же палец для 3+ символов - неудобно
                return {
                    'comfort': 'uncomfortable',
                    'reason': 'same_finger_multiple',
                    'hand_type': hand_type,
                    'sequence': sequence,
                    'length': len(sequence),
                    'has_modifiers': any(a['is_modifier'] for a in all_actions)
                }
            
            # Анализируем направление движения
            directions = []
            for i in range(len(key_actions) - 1):
                action1, action2 = key_actions[i], key_actions[i+1]
                order1 = self.get_finger_order(action1['finger'])
                order2 = self.get_finger_order(action2['finger'])
                
                if order1 == 0 or order2 == 0:
                    directions.append('unknown')
                elif order1 < order2:
                    directions.append('outside_to_inside')  # удобное направление
                elif order1 > order2:
                    directions.append('inside_to_outside')  # частично удобное направление
                else:
                    directions.append('same_finger')
            
            # Если есть неизвестные направления
            if 'unknown' in directions:
                return {'comfort': 'unknown', 'reason': 'unknown_direction'}
            
            # Определяем тип последовательности
            direction_changes = 0
            for i in range(len(directions) - 1):
                if directions[i] != directions[i+1]:
                    direction_changes += 1
            
            if direction_changes > 0:
                # Смена направления - НЕУДОБНО
                return {
                    'comfort': 'uncomfortable',
                    'reason': 'direction_changes',
                    'hand_type': hand_type,
                    'sequence': sequence,
                    'length': len(sequence),
                    'direction_changes': direction_changes,
                    'has_modifiers': any(a['is_modifier'] for a in all_actions)
                }
            else:
                # Все движения в одном направлении
                first_direction = directions[0]
                if first_direction == 'outside_to_inside':
                    # Все движения от мизинца к указательному - УДОБНО
                    return {
                        'comfort': 'comfortable',
                        'reason': 'all_outside_to_inside',
                        'hand_type': hand_type,
                        'sequence': sequence,
                        'length': len(sequence),
                        'has_modifiers': any(a['is_modifier'] for a in all_actions)
                    }
                elif first_direction == 'inside_to_outside':
                    # Все движения от указательного к мизинцу - ЧАСТИЧНО УДОБНО
                    return {
                        'comfort': 'partial',
                        'reason': 'all_inside_to_outside',
                        'hand_type': hand_type,
                        'sequence': sequence,
                        'length': len(sequence),
                        'has_modifiers': any(a['is_modifier'] for a in all_actions)
                    }
                else:
                    # Все на одном пальце - неудобно для 3+ символов
                    return {
                        'comfort': 'uncomfortable',
                        'reason': 'all_same_finger',
                        'hand_type': hand_type,
                        'sequence': sequence,
                        'length': len(sequence),
                        'has_modifiers': any(a['is_modifier'] for a in all_actions)
                    }
    
    # Обновляем метод analyze_sequence_comfort для использования новой логики
    def analyze_sequence_comfort(self, sequence: str) -> Dict[str, Any]:
        """Обертка для обратной совместимости"""
        return self.analyze_sequence_comfort_with_modifiers(sequence)
    
    def calculate_modifier_statistics(self) -> Dict[str, Any]:
        """
        Рассчитывает статистику по использованию модификаторов
        """
        modifier_stats = {
            'total_symbols': 0,
            'with_shift': 0,
            'with_alt': 0,
            'with_both': 0,
            'no_modifiers': 0,
            'shift_percent': 0,
            'alt_percent': 0
        }
        
        for letter, modifiers in self.modifiers_map.items():
            modifier_stats['total_symbols'] += 1
            
            if not modifiers:
                modifier_stats['no_modifiers'] += 1
            else:
                # Проверяем наличие модификаторов
                has_shift = any(isinstance(mod, str) and mod == "shift" for mod in modifiers)
                has_alt = any(isinstance(mod, str) and mod == "alt" for mod in modifiers)
                
                if has_shift and has_alt:
                    modifier_stats['with_both'] += 1
                elif has_shift:
                    modifier_stats['with_shift'] += 1
                elif has_alt:
                    modifier_stats['with_alt'] += 1
        
        if modifier_stats['total_symbols'] > 0:
            modifier_stats['shift_percent'] = (modifier_stats['with_shift'] / modifier_stats['total_symbols']) * 100
            modifier_stats['alt_percent'] = (modifier_stats['with_alt'] / modifier_stats['total_symbols']) * 100
        
        return modifier_stats
    
    def analyze_word_sequences(self, word: str) -> Dict[str, Any]:
        """
        Анализ всех последовательностей в слове (от 2 до 5 символов)
        """
        word = word.strip()
        
        # Пропускаем односимвольные слова
        if len(word) < 2:
            return None
        
        # Проверяем, что слово содержит допустимые символы
        # Добавляем проверку наличия символов в раскладке
        valid_chars = []
        for char in word:
            if char in self.position_map:
                valid_chars.append(char)
        
        if len(valid_chars) < 2:
            return None
        
        result = {
            'word': word,
            'word_length': len(word),
            'valid_chars': len(valid_chars),
            'sequences_by_length': {
                2: {'total': 0, 'comfortable': 0, 'partial': 0, 'uncomfortable': 0, 'details': []},
                3: {'total': 0, 'comfortable': 0, 'partial': 0, 'uncomfortable': 0, 'details': []},
                4: {'total': 0, 'comfortable': 0, 'partial': 0, 'uncomfortable': 0, 'details': []},
                5: {'total': 0, 'comfortable': 0, 'partial': 0, 'uncomfortable': 0, 'details': []}
            },
            'total_sequences': 0,
            'sequences_with_modifiers': 0
        }
        
        # Анализируем последовательности всех длин
        for seq_len in [2, 3, 4, 5]:
            if len(valid_chars) >= seq_len:
                for i in range(len(valid_chars) - seq_len + 1):
                    sequence = ''.join(valid_chars[i:i + seq_len])
                    analysis = self.analyze_sequence_comfort_with_modifiers(sequence)
                    
                    if analysis['comfort'] != 'unknown':
                        result['sequences_by_length'][seq_len]['total'] += 1
                        result['sequences_by_length'][seq_len][analysis['comfort']] += 1
                        result['sequences_by_length'][seq_len]['details'].append(analysis)
                        result['total_sequences'] += 1
                        
                        if analysis.get('has_modifiers', False):
                            result['sequences_with_modifiers'] += 1
        
        return result
    
    def calculate_finger_load_and_distance(self) -> Dict[str, Any]:
        """
        Рассчитывает нагрузку на пальцы и максимальное расстояние
        с учетом модификаторов
        """
        finger_counter = Counter()
        finger_positions = defaultdict(list)
        
        # Собираем статистику по всем символам в раскладке
        for letter, data in self.layout_data.items():
            # Определяем параметры в зависимости от формата данных
            if isinstance(data, dict):
                finger = data.get("finger", "")
                row = data.get("row", 0)
                column = data.get("column", 0)
                modifiers = data.get("modifiers", [])
            elif isinstance(data, list):
                finger = str(data[1]) if len(data) > 1 else ""
                row = int(data[2]) if len(data) > 2 else 0
                column = int(data[3]) if len(data) > 3 else 0
                modifiers = data[4:] if len(data) > 4 else []
            else:
                continue
            
            if finger:
                # Учитываем основной символ
                finger_counter[finger] += 1
                finger_positions[finger].append((row, column, letter, False))
                
                # Учитываем модификаторы
                for modifier in modifiers:
                    if isinstance(modifier, str) and modifier == "shift":
                        # Shift на той же руке
                        if isinstance(data, dict):
                            hand = data.get("hand", "").lower()
                        else:
                            hand = str(data[0]).lower() if data[0] else ""
                        shift_finger = "L1" if hand == "left" else "R4"
                        finger_counter[shift_finger] += 0.5  # Shift учитываем с весом 0.5
                    elif isinstance(modifier, str) and modifier == "alt":
                        # Alt всегда правой рукой
                        finger_counter["R4"] += 0.5  # Alt учитываем с весом 0.5
        
        # Рассчитываем нагрузку на пальцы
        total_weight = sum(finger_counter.values())
        finger_load = {}
        for finger, weight in finger_counter.items():
            finger_load[finger] = (weight / total_weight * 100) if total_weight > 0 else 0
        
        # Находим два самых загруженных пальца
        sorted_fingers = sorted(finger_load.items(), key=lambda x: x[1], reverse=True)
        top_two_load = sum(load for _, load in sorted_fingers[:2])
        
        # Рассчитываем максимальное расстояние для каждого пальца (только для основных символов)
        max_distances = {}
        for finger, positions in finger_positions.items():
            if len(positions) > 1:
                distances = []
                for i in range(len(positions)):
                    for j in range(i + 1, len(positions)):
                        row1, col1, _, _ = positions[i]
                        row2, col2, _, _ = positions[j]
                        # Манхэттенское расстояние
                        distance = abs(row2 - row1) + abs(col2 - col1)
                        distances.append(distance)
                max_distances[finger] = max(distances) if distances else 0
            else:
                max_distances[finger] = 0
        
        overall_max_distance = max(max_distances.values()) if max_distances else 0
        
        # Рассчитываем общую "лучшесть"
        normalized_load = top_two_load / 100
        normalized_distance = overall_max_distance / 20
        
        goodness_score = normalized_load + normalized_distance
        
        return {
            'finger_load': dict(finger_load),
            'top_two_fingers_load': top_two_load,
            'max_distances': dict(max_distances),
            'overall_max_distance': overall_max_distance,
            'goodness_score': goodness_score,
            'normalized_score': 1 / (1 + goodness_score),
            'modifier_stats': self.calculate_modifier_statistics()
        }
    
    def calculate_comprehensive_analysis(self, wordlist: List[str]) -> Dict[str, Any]:
        """
        Комплексный анализ для всего списка слов
        """
        total_stats = {
            'layout_name': self.layout_name,
            'by_length': {
                2: {'total': 0, 'comfortable': 0, 'partial': 0, 'uncomfortable': 0},
                3: {'total': 0, 'comfortable': 0, 'partial': 0, 'uncomfortable': 0},
                4: {'total': 0, 'comfortable': 0, 'partial': 0, 'uncomfortable': 0},
                5: {'total': 0, 'comfortable': 0, 'partial': 0, 'uncomfortable': 0}
            },
            'total_sequences': 0,
            'total_words': len(wordlist),
            'words_analyzed': 0,
            'sequences_with_modifiers': 0,
            'sequence_frequencies': {
                'comfortable': Counter(),
                'partial': Counter(),
                'uncomfortable': Counter()
            },
            'comfort_examples': {
                'comfortable': [],
                'partial': [],
                'uncomfortable': []
            },
            'finger_analysis': self.calculate_finger_load_and_distance()
        }
        
        for word in tqdm(wordlist, desc=f"Анализ раскладки {self.layout_name}"):
            analysis = self.analyze_word_sequences(word)
            
            if analysis is None:
                continue
            
            total_stats['words_analyzed'] += 1
            
            # Агрегируем статистику по длинам
            for seq_len in [2, 3, 4, 5]:
                length_data = analysis['sequences_by_length'][seq_len]
                for comfort_type in ['comfortable', 'partial', 'uncomfortable']:
                    total_stats['by_length'][seq_len][comfort_type] += length_data[comfort_type]
                    total_stats['by_length'][seq_len]['total'] += length_data[comfort_type]
            
            total_stats['total_sequences'] += analysis['total_sequences']
            total_stats['sequences_with_modifiers'] += analysis.get('sequences_with_modifiers', 0)
            
            # Собираем примеры и частоты для каждого типа удобства
            for seq_len in [2, 3, 4, 5]:
                for seq_analysis in analysis['sequences_by_length'][seq_len]['details']:
                    comfort_type = seq_analysis['comfort']
                    seq_str = seq_analysis['sequence']
                    
                    # Собираем частоты
                    total_stats['sequence_frequencies'][comfort_type][seq_str] += 1
                    
                    # Собираем уникальные примеры
                    if seq_str not in [ex['sequence'] for ex in total_stats['comfort_examples'][comfort_type]]:
                        if len(total_stats['comfort_examples'][comfort_type]) < 10:
                            total_stats['comfort_examples'][comfort_type].append(seq_analysis)
        
        # Рассчитываем проценты
        for seq_len in [2, 3, 4, 5]:
            total = total_stats['by_length'][seq_len]['total']
            if total > 0:
                for comfort_type in ['comfortable', 'partial', 'uncomfortable']:
                    count = total_stats['by_length'][seq_len][comfort_type]
                    total_stats['by_length'][seq_len][f'{comfort_type}_percent'] = (count / total) * 100
        
        # Рассчитываем общую статистику
        total_comfortable = sum(total_stats['by_length'][l]['comfortable'] for l in [2, 3, 4, 5])
        total_partial = sum(total_stats['by_length'][l]['partial'] for l in [2, 3, 4, 5])
        total_uncomfortable = sum(total_stats['by_length'][l]['uncomfortable'] for l in [2, 3, 4, 5])
        
        total_stats['overall'] = {
            'comfortable': total_comfortable,
            'partial': total_partial,
            'uncomfortable': total_uncomfortable,
            'total': total_stats['total_sequences'],
            'comfortable_percent': (total_comfortable / total_stats['total_sequences'] * 100) if total_stats['total_sequences'] > 0 else 0,
            'partial_percent': (total_partial / total_stats['total_sequences'] * 100) if total_stats['total_sequences'] > 0 else 0,
            'uncomfortable_percent': (total_uncomfortable / total_stats['total_sequences'] * 100) if total_stats['total_sequences'] > 0 else 0,
            'modifiers_percent': (total_stats['sequences_with_modifiers'] / total_stats['total_sequences'] * 100) if total_stats['total_sequences'] > 0 else 0
        }
        
        # Сортируем последовательности по частоте для каждого типа
        for comfort_type in ['comfortable', 'partial', 'uncomfortable']:
            total_stats[f'top_{comfort_type}_sequences'] = dict(
                sorted(total_stats['sequence_frequencies'][comfort_type].items(), 
                      key=lambda x: x[1], reverse=True)[:20]
            )
        
        del total_stats['sequence_frequencies']
        
        return total_stats
    
    def prepare_plot_data(self, comprehensive_stats: Dict[str, Any]) -> Dict[str, Any]:
        """
        Подготавливает данные в формате для построения графиков
        """
        plot_data = {
            'layout_name': self.layout_name,
            'by_length': {
                'lengths': ['2 символа', '3 символа', '4 символа', '5 символов'],
                'comfortable': [],
                'partial': [],
                'uncomfortable': [],
                'comfortable_percent': [],
                'partial_percent': [],
                'uncomfortable_percent': [],
                'total': []
            },
            'overall_stats': {
                'comfortable': comprehensive_stats['overall']['comfortable'],
                'partial': comprehensive_stats['overall']['partial'],
                'uncomfortable': comprehensive_stats['overall']['uncomfortable'],
                'comfortable_percent': comprehensive_stats['overall']['comfortable_percent'],
                'partial_percent': comprehensive_stats['overall']['partial_percent'],
                'uncomfortable_percent': comprehensive_stats['overall']['uncomfortable_percent'],
                'modifiers_percent': comprehensive_stats['overall']['modifiers_percent'],
                'total_sequences': comprehensive_stats['overall']['total']
            },
            'finger_analysis': comprehensive_stats['finger_analysis'],
            'examples': comprehensive_stats['comfort_examples'],
            'top_sequences': {
                'comfortable': comprehensive_stats.get('top_comfortable_sequences', {}),
                'partial': comprehensive_stats.get('top_partial_sequences', {}),
                'uncomfortable': comprehensive_stats.get('top_uncomfortable_sequences', {})
            },
            'word_stats': {
                'total_words': comprehensive_stats['total_words'],
                'words_analyzed': comprehensive_stats['words_analyzed'],
                'analysis_percent': (comprehensive_stats['words_analyzed'] / comprehensive_stats['total_words'] * 100) 
                                   if comprehensive_stats['total_words'] > 0 else 0
            }
        }
        
        # Заполняем данные по длинам
        for length in [2, 3, 4, 5]:
            data = comprehensive_stats['by_length'][length]
            plot_data['by_length']['comfortable'].append(data['comfortable'])
            plot_data['by_length']['partial'].append(data['partial'])
            plot_data['by_length']['uncomfortable'].append(data['uncomfortable'])
            plot_data['by_length']['comfortable_percent'].append(data.get('comfortable_percent', 0))
            plot_data['by_length']['partial_percent'].append(data.get('partial_percent', 0))
            plot_data['by_length']['uncomfortable_percent'].append(data.get('uncomfortable_percent', 0))
            plot_data['by_length']['total'].append(data['total'])
        
        return plot_data


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

def analyze_layout_comprehensive(layout_config: Dict[str, Any], 
                               layout_name: str,
                               file_path: str,
                               max_samples: int = 100000) -> Dict[str, Any]:
    """
    Комплексный анализ раскладки
    """
    analyzer = LayoutAnalyzer(layout_config, layout_name)
    
    # Собираем слова для анализа
    words_for_analysis = []
    word_generator = read_words_by_lines(file_path, batch_size=1000, encoding='utf-8')
    
    total_words = count_lines_in_file(file_path, encoding='utf-8')
    pbar = tqdm(total=min(total_words, max_samples), desc=f"Сбор слов для {layout_name}")
    
    try:
        for batch in word_generator:
            for word in batch:
                if len(words_for_analysis) < max_samples:
                    word = word.strip()
                    if len(word) >= 2:
                        words_for_analysis.append(word)
                        pbar.update(1)
                
                if len(words_for_analysis) >= max_samples:
                    break
            if len(words_for_analysis) >= max_samples:
                break
    finally:
        pbar.close()
    
    print(f"\n📊 Для раскладки '{layout_name}':")
    print(f"   • Собрано слов: {len(words_for_analysis):,}")
    
    # Выполняем комплексный анализ
    comprehensive_stats = analyzer.calculate_comprehensive_analysis(words_for_analysis)
    
    # Подготавливаем данные для графиков
    plot_data = analyzer.prepare_plot_data(comprehensive_stats)
    
    # Формируем итоговый результат
    result = {
        'layout_name': layout_name,
        'file_analyzed': os.path.basename(file_path),
        'total_words_in_file': total_words,
        'words_analyzed': len(words_for_analysis),
        'comprehensive_stats': comprehensive_stats,
        'plot_data': plot_data,
        'goodness_score': comprehensive_stats['finger_analysis']['goodness_score'],
        'normalized_score': comprehensive_stats['finger_analysis']['normalized_score']
    }
    
    return result

def print_analysis_summary(result):
    """
    Выводит сводку анализа
    """
    layout_name = result['layout_name']
    plot_data = result['plot_data']
    finger_analysis = result['comprehensive_stats']['finger_analysis']
    modifier_stats = finger_analysis.get('modifier_stats', {})
    
    print("\n" + "=" * 80)
    print(f"АНАЛИЗ РАСКЛАДКИ: {layout_name}")
    print("=" * 80)
    
    print(f"\n📊 ОБЩАЯ СТАТИСТИКА:")
    print(f"  • Файл: {result['file_analyzed']}")
    print(f"  • Всего слов в файле: {result['total_words_in_file']:,}")
    print(f"  • Проанализировано слов: {result['words_analyzed']:,}")
    print(f"  • Всего последовательностей: {plot_data['overall_stats']['total_sequences']:,}")
    
    print(f"\n🏆 ЛУЧШЕСТЬ РАСКЛАДКИ (по критерию 'путь пальца'):")
    print(f"  • Нагрузка на два самых загруженных пальца: {finger_analysis['top_two_fingers_load']:.1f}%")
    print(f"  • Максимальный путь пальца: {finger_analysis['overall_max_distance']:.2f}")
    print(f"  • Goodness Score: {finger_analysis['goodness_score']:.4f}")
    print(f"  • Нормализованный Score (чем ближе к 1, тем лучше): {finger_analysis['normalized_score']:.4f}")
    
    print(f"\n🎯 СТАТИСТИКА ПО МОДИФИКАТОРАМ:")
    if modifier_stats:
        print(f"  • Всего символов в раскладке: {modifier_stats['total_symbols']}")
        print(f"  • Символов с Shift: {modifier_stats['with_shift']} ({modifier_stats['shift_percent']:.1f}%)")
        print(f"  • Символов с Alt: {modifier_stats['with_alt']} ({modifier_stats['alt_percent']:.1f}%)")
        print(f"  • Символов с обоими модификаторами: {modifier_stats['with_both']}")
        print(f"  • Последовательностей с модификаторами: {plot_data['overall_stats']['modifiers_percent']:.1f}%")
    
    print(f"\n📈 ОБЩАЯ УДОБНОСТЬ ПОСЛЕДОВАТЕЛЬНОСТЕЙ:")
    print(f"  • Удобные: {plot_data['overall_stats']['comfortable']:,} ({plot_data['overall_stats']['comfortable_percent']:.1f}%)")
    print(f"  • Частично удобные: {plot_data['overall_stats']['partial']:,} ({plot_data['overall_stats']['partial_percent']:.1f}%)")
    print(f"  • Неудобные: {plot_data['overall_stats']['uncomfortable']:,} ({plot_data['overall_stats']['uncomfortable_percent']:.1f}%)")
    
    print(f"\n📏 СТАТИСТИКА ПО ДЛИНАМ ПОСЛЕДОВАТЕЛЬНОСТЕЙ:")
    for i, length_name in enumerate(plot_data['by_length']['lengths']):
        print(f"  • {length_name}:")
        print(f"      Удобные: {plot_data['by_length']['comfortable'][i]:,} ({plot_data['by_length']['comfortable_percent'][i]:.1f}%)")
        print(f"      Частично удобные: {plot_data['by_length']['partial'][i]:,} ({plot_data['by_length']['partial_percent'][i]:.1f}%)")
        print(f"      Неудобные: {plot_data['by_length']['uncomfortable'][i]:,} ({plot_data['by_length']['uncomfortable_percent'][i]:.1f}%)")
        print(f"      Всего: {plot_data['by_length']['total'][i]:,}")
    
    print(f"\n👆 НАГРУЗКА НА ПАЛЬЦЫ:")
    for finger, load in finger_analysis['finger_load'].items():
        print(f"  • {finger}: {load:.1f}%")
    
    # Примеры для каждого типа удобства
    for comfort_type, comfort_name in [('comfortable', 'Удобные'), ('partial', 'Частично удобные'), ('uncomfortable', 'Неудобные')]:
        examples = plot_data['examples'].get(comfort_type, [])
        if examples:
            print(f"\n{'✅' if comfort_type == 'comfortable' else '⚠️' if comfort_type == 'partial' else '❌'} ПРИМЕРЫ {comfort_name.upper()} ПОСЛЕДОВАТЕЛЬНОСТЕЙ:")
            for example in examples[:3]:
                has_mod = example.get('has_modifiers', False)
                mod_info = " (с модификаторами)" if has_mod else ""
                reason_map = {
                    'outside_to_inside': 'внешние→внутренние',
                    'inside_to_outside': 'внутренние→внешние',
                    'same_finger': 'один палец',
                    'hand_change_with_modifiers': 'смена руки (с модиф.)',
                    'direction_changes': 'смена направления',
                    'same_characters': 'одинаковые символы'
                }
                reason = reason_map.get(example.get('reason', ''), example.get('reason', 'неизвестно'))
                print(f"  • '{example['sequence']}' ({example['length']} символа){mod_info} - {reason}")
    
    print(f"\n🏆 ТОП-3 САМЫХ ЧАСТЫХ УДОБНЫХ ПОСЛЕДОВАТЕЛЬНОСТЕЙ:")
    top_comfortable = list(plot_data['top_sequences']['comfortable'].items())[:3]
    for i, (seq, freq) in enumerate(top_comfortable, 1):
        print(f"  {i}. '{seq}': {freq:,} раз")
    
    print(f"\n🏆 ТОП-3 САМЫХ ЧАСТЫХ ЧАСТИЧНО УДОБНЫХ ПОСЛЕДОВАТЕЛЬНОСТЕЙ:")
    top_partial = list(plot_data['top_sequences']['partial'].items())[:3]
    for i, (seq, freq) in enumerate(top_partial, 1):
        print(f"  {i}. '{seq}': {freq:,} раз")
    
    print("\n" + "=" * 80)
    print("АНАЛИЗ ЗАВЕРШЕН!")
    print("=" * 80)

def save_analysis_results(result, output_dir: str = "analysis_results"):
    """Сохраняет результаты анализа в JSON файл с названием раскладки"""
    os.makedirs(output_dir, exist_ok=True)
    
    layout_name = result['layout_name']
    # Убираем недопустимые символы для имени файла
    safe_name = "".join(c for c in layout_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
    output_file = os.path.join(output_dir, f"{safe_name}_analysis.json")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"💾 Результаты сохранены в: {output_file}")
    return output_file

def analyze_multiple_layouts(layout_files: List[Tuple[str, str]], 
                           text_file: str,
                           max_samples_per_layout: int = 100000) -> Dict[str, Any]:
    """
    Анализирует несколько раскладок и сравнивает результаты
    """
    all_results = {}
    comparison_data = {
        'layouts': [],
        'by_length_comparison': {
            2: {'layouts': [], 'comfortable': [], 'partial': [], 'uncomfortable': []},
            3: {'layouts': [], 'comfortable': [], 'partial': [], 'uncomfortable': []},
            4: {'layouts': [], 'comfortable': [], 'partial': [], 'uncomfortable': []},
            5: {'layouts': [], 'comfortable': [], 'partial': [], 'uncomfortable': []}
        },
        'goodness_scores': [],
        'overall_comfort': {'layouts': [], 'comfortable': [], 'partial': [], 'uncomfortable': []},
        'modifier_stats': [],
        'text_file': os.path.basename(text_file),
        'total_words_analyzed': 0
    }
    
    for layout_file, layout_name in layout_files:
        print(f"\n{'='*60}")
        print(f"НАЧИНАЕМ АНАЛИЗ РАСКЛАДКИ: {layout_name}")
        print(f"{'='*60}")
        
        try:
            layout_config = load_layout_from_json(layout_file)
            result = analyze_layout_comprehensive(
                layout_config, 
                layout_name, 
                text_file,
                max_samples_per_layout
            )
            
            all_results[layout_name] = result
            
            # Сохраняем результаты для сравнения
            comparison_data['layouts'].append(layout_name)
            comparison_data['total_words_analyzed'] += result['words_analyzed']
            
            # Данные по длинам для сравнения
            for length in [2, 3, 4, 5]:
                plot_data = result['plot_data']
                idx = list(plot_data['by_length']['lengths']).index(f'{length} символа' if length != 5 else '5 символов')
                
                comparison_data['by_length_comparison'][length]['layouts'].append(layout_name)
                comparison_data['by_length_comparison'][length]['comfortable'].append(
                    plot_data['by_length']['comfortable_percent'][idx]
                )
                comparison_data['by_length_comparison'][length]['partial'].append(
                    plot_data['by_length']['partial_percent'][idx]
                )
                comparison_data['by_length_comparison'][length]['uncomfortable'].append(
                    plot_data['by_length']['uncomfortable_percent'][idx]
                )
            
            # Общая удобность
            comparison_data['overall_comfort']['layouts'].append(layout_name)
            comparison_data['overall_comfort']['comfortable'].append(
                result['plot_data']['overall_stats']['comfortable_percent']
            )
            comparison_data['overall_comfort']['partial'].append(
                result['plot_data']['overall_stats']['partial_percent']
            )
            comparison_data['overall_comfort']['uncomfortable'].append(
                result['plot_data']['overall_stats']['uncomfortable_percent']
            )
            
            # Goodness scores
            comparison_data['goodness_scores'].append({
                'layout': layout_name,
                'score': result['goodness_score'],
                'normalized': result['normalized_score'],
                'top_two_load': result['comprehensive_stats']['finger_analysis']['top_two_fingers_load'],
                'max_distance': result['comprehensive_stats']['finger_analysis']['overall_max_distance']
            })
            
            # Статистика по модификаторам
            modifier_stats = result['comprehensive_stats']['finger_analysis'].get('modifier_stats', {})
            comparison_data['modifier_stats'].append({
                'layout': layout_name,
                'shift_percent': modifier_stats.get('shift_percent', 0),
                'alt_percent': modifier_stats.get('alt_percent', 0),
                'sequences_with_modifiers': result['plot_data']['overall_stats'].get('modifiers_percent', 0)
            })
            
            # Выводим сводку
            print_analysis_summary(result)
            
            # Сохраняем результаты
            save_analysis_results(result)
            
        except Exception as e:
            print(f"❌ Ошибка при анализе раскладки {layout_name}: {str(e)}")
            import traceback
            traceback.print_exc()
            continue
    
    # Сохраняем данные для сравнения
    comparison_file = os.path.join("analysis_results", "layout_comparison.json")
    with open(comparison_file, 'w', encoding='utf-8') as f:
        json.dump(comparison_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Данные для сравнения сохранены в: {comparison_file}")
    
    # Выводим итоговое сравнение
    print("\n" + "="*80)
    print("ИТОГОВОЕ СРАВНЕНИЕ РАСКЛАДОК")
    print("="*80)
    
    if comparison_data['goodness_scores']:
        print("\n🏆 РЕЙТИНГ РАСКЛАДОК (чем меньше goodness score, тем лучше):")
        sorted_scores = sorted(comparison_data['goodness_scores'], key=lambda x: x['score'])
        for i, score_data in enumerate(sorted_scores, 1):
            print(f"{i}. {score_data['layout']}:")
            print(f"   • Goodness Score: {score_data['score']:.4f}")
            print(f"   • Нормализованный: {score_data['normalized']:.4f}")
            print(f"   • Нагрузка на 2 пальца: {score_data['top_two_load']:.1f}%")
            print(f"   • Макс. расстояние: {score_data['max_distance']:.2f}")
    
    if comparison_data['modifier_stats']:
        print("\n🎯 СТАТИСТИКА ПО МОДИФИКАТОРАМ:")
        for stats in comparison_data['modifier_stats']:
            print(f"  • {stats['layout']}: Shift={stats['shift_percent']:.1f}%, Alt={stats['alt_percent']:.1f}%, Послед. с модиф.={stats['sequences_with_modifiers']:.1f}%")
    
    return {
        'individual_results': all_results,
        'comparison_data': comparison_data
    }

if __name__ == "__main__":
    # Определяем раскладки для анализа
    LAYOUTS = [
        ("/Users/evgenii/Develop/py_proj/tr/KVA/example_layouts/йцукен (2).json", "ЙЦУКЕН (стандартная)"),
        ("/Users/evgenii/Develop/py_proj/tr/KVA/example_layouts/ant (4).json", "Альтернативная раскладка"),
        ("/Users/evgenii/Develop/py_proj/tr/KVA/example_layouts/rusphone (2).json","русфон"),
        ("/Users/evgenii/Develop/py_proj/tr/KVA/example_layouts/zubachew.json","зубачев"),
        ("/Users/evgenii/Develop/py_proj/tr/KVA/example_layouts/skoropis (2).json","скоропись"),
        ("/Users/evgenii/Develop/py_proj/tr/KVA/example_layouts/diktor (2).json","диктор"),
        ("/Users/evgenii/Develop/py_proj/tr/KVA/example_layouts/keyboardFINAL (1).json","Вызов"),
        # Добавьте другие раскладки здесь
    ]
    
    # Файл с текстом для анализа
    TEXT_FILE = "/Users/evgenii/Develop/py_proj/tr/KVA/1grams-3.txt"
    
    # Проверяем существование файлов раскладок
    valid_layouts = []
    for layout_file, layout_name in LAYOUTS:
        if os.path.exists(layout_file):
            valid_layouts.append((layout_file, layout_name))
        else:
            print(f"⚠️  Файл раскладки не найден: {layout_file}")
    
    if not valid_layouts:
        print("❌ Не найдено ни одной валидной раскладки для анализа")
    else:
        # Анализируем все раскладки
        results = analyze_multiple_layouts(
            valid_layouts,
            TEXT_FILE,
            max_samples_per_layout=500000  
        )
        
        print("\n🎯 АНАЛИЗ ВСЕХ РАСКЛАДОК ЗАВЕРШЕН!")