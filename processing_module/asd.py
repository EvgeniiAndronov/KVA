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
        self.column_map = {}  # Буква -> столбец
        
        self._parse_layout()
    
    def _parse_layout(self):
        """Парсит конфигурацию раскладки и создает маппинги"""
        for letter, data in self.layout_data.items():
            if len(data) >= 3:
                hand, row, col = data[0], data[1], data[2]
                self.hand_map[letter] = hand
                self.position_map[letter] = (hand, row, col)
                self.column_map[letter] = col
                finger = self._get_finger_for_column(hand, col)
                self.finger_map[letter] = finger
    
    def _get_finger_for_column(self, hand: str, column: int) -> str:
        """Определяет палец для столбца"""
        if column <= 2:
            return f"{hand}y"  # указательный
        elif column <= 4:
            return f"{hand}s"  # средний
        elif column <= 6:
            return f"{hand}b"  # безымянный
        else:
            return f"{hand}m"  # мизинец
    
    def analyze_sequence_comfort_new_logic(self, sequence: str) -> Dict[str, Any]:
        """
        Анализирует удобство последовательности по НОВОЙ логике:
        - Разные руки → НЕУДОБНО ❌
        - Левая рука: удобно когда столбцы ВОЗРАСТАЮТ (мизинец → указательный)
        - Правая рука: удобно когда столбцы УБЫВАЮТ (мизинец → указательный)
        - Один палец → НЕУДОБНО ❌
        """
        if len(sequence) < 2:
            return {'comfort': 'unknown', 'reason': 'too_short'}
        
        # Проверяем, что все символы есть в раскладке
        if not all(char in self.position_map for char in sequence):
            return {'comfort': 'unknown', 'reason': 'unknown_chars'}
        
        hands = [self.hand_map[char] for char in sequence]
        unique_hands = set(hands)
        
        # Разные руки - НЕУДОБНО ❌
        if len(unique_hands) > 1:
            return {
                'comfort': 'uncomfortable',
                'reason': 'different_hands',
                'hand_type': 'both',
                'sequence': sequence,
                'length': len(sequence)
            }
        
        # Одна рука
        hand_type = 'left' if list(unique_hands)[0] == 'l' else 'right'
        
        # Проверяем последовательность на одном пальце
        fingers = [self.finger_map[char] for char in sequence]
        if len(set(fingers)) == 1:
            return {
                'comfort': 'uncomfortable',
                'reason': 'same_finger',
                'hand_type': hand_type,
                'sequence': sequence,
                'length': len(sequence)
            }
        
        # Анализируем направление для последовательности из 2+ символов
        if len(sequence) >= 2:
            comfort_level = self._analyze_direction_comfort(sequence, hand_type)
            return {
                'comfort': comfort_level,
                'reason': 'direction_analysis',
                'hand_type': hand_type,
                'sequence': sequence,
                'length': len(sequence)
            }
        
        return {'comfort': 'unknown', 'reason': 'unable_to_analyze'}
    
    def _analyze_direction_comfort(self, sequence: str, hand_type: str) -> str:
        """
        Анализирует удобство направления для последовательности
        """
        comfortable_moves = 0
        total_moves = len(sequence) - 1
        
        for i in range(total_moves):
            char1, char2 = sequence[i], sequence[i+1]
            col1, col2 = self.column_map[char1], self.column_map[char2]
            
            # Определяем удобное направление
            if hand_type == 'left':
                # Левая рука: удобно когда столбцы ВОЗРАСТАЮТ
                is_comfortable = col2 > col1
            else:
                # Правая рука: удобно когда столбцы УБЫВАЮТ  
                is_comfortable = col2 < col1
            
            if is_comfortable:
                comfortable_moves += 1
        
        # Определяем общий уровень удобства
        comfort_ratio = comfortable_moves / total_moves if total_moves > 0 else 0
        
        if comfort_ratio >= 0.8:  # 80%+ удобных движений
            return 'comfortable'
        elif comfort_ratio >= 0.5:  # 50-79% удобных движений
            return 'partial'
        else:  # Менее 50% удобных движений
            return 'uncomfortable'
    
    def analyze_word_sequences_comprehensive(self, word: str) -> Dict[str, Any]:
        """
        Комплексный анализ всех последовательностей в слове
        Возвращает данные для графиков
        """
        result = {
            'word': word,
            'word_length': len(word),
            'sequences_by_length': {
                2: {'total': 0, 'comfortable': 0, 'partial': 0, 'uncomfortable': 0, 'details': []},
                3: {'total': 0, 'comfortable': 0, 'partial': 0, 'uncomfortable': 0, 'details': []},
                4: {'total': 0, 'comfortable': 0, 'partial': 0, 'uncomfortable': 0, 'details': []},
                5: {'total': 0, 'comfortable': 0, 'partial': 0, 'uncomfortable': 0, 'details': []}
            },
            'sequences_by_hand': {
                'left': {'total': 0, 'comfortable': 0, 'partial': 0, 'uncomfortable': 0},
                'right': {'total': 0, 'comfortable': 0, 'partial': 0, 'uncomfortable': 0},
                'both': {'total': 0, 'comfortable': 0, 'partial': 0, 'uncomfortable': 0}
            },
            'sequence_frequencies': Counter(),
            'covers_whole_word': False
        }
        
        # Анализируем последовательности всех длин
        for seq_len in [2, 3, 4, 5]:
            if len(word) >= seq_len:
                # Проверяем, покрывает ли последовательность всё слово
                if len(word) == seq_len:
                    result['covers_whole_word'] = True
                
                for i in range(len(word) - seq_len + 1):
                    sequence = word[i:i + seq_len]
                    analysis = self.analyze_sequence_comfort_new_logic(sequence)
                    
                    if analysis['comfort'] != 'unknown':
                        # Обновляем статистику по длине
                        result['sequences_by_length'][seq_len]['total'] += 1
                        result['sequences_by_length'][seq_len][analysis['comfort']] += 1
                        result['sequences_by_length'][seq_len]['details'].append(analysis)
                        
                        # Обновляем статистику по рукам
                        hand_type = analysis.get('hand_type', 'both')
                        result['sequences_by_hand'][hand_type]['total'] += 1
                        result['sequences_by_hand'][hand_type][analysis['comfort']] += 1
                        
                        # Собираем частоты
                        result['sequence_frequencies'][sequence] += 1
        
        # Преобразуем Counter в dict
        result['sequence_frequencies'] = dict(result['sequence_frequencies'])
        
        return result
    
    def calculate_comprehensive_analysis(self, wordlist: List[str]) -> Dict[str, Any]:
        """
        Комплексный анализ для всего списка слов
        Возвращает данные для всех графиков
        """
        total_stats = {
            'by_length': {
                2: {'total': 0, 'comfortable': 0, 'partial': 0, 'uncomfortable': 0},
                3: {'total': 0, 'comfortable': 0, 'partial': 0, 'uncomfortable': 0},
                4: {'total': 0, 'comfortable': 0, 'partial': 0, 'uncomfortable': 0},
                5: {'total': 0, 'comfortable': 0, 'partial': 0, 'uncomfortable': 0}
            },
            'by_hand': {
                'left': {'total': 0, 'comfortable': 0, 'partial': 0, 'uncomfortable': 0},
                'right': {'total': 0, 'comfortable': 0, 'partial': 0, 'uncomfortable': 0},
                'both': {'total': 0, 'comfortable': 0, 'partial': 0, 'uncomfortable': 0}
            },
            'word_coverage': {
                'words_with_full_coverage': 0,  # Слова полностью покрытые последовательностями
                'total_words': len(wordlist)
            },
            'sequence_frequencies': Counter(),
            'comfort_examples': {
                'comfortable': [],
                'partial': [],
                'uncomfortable': []
            },
            'word_length_stats': defaultdict(int)
        }
        
        for word in tqdm(wordlist, desc="Комплексный анализ"):
            analysis = self.analyze_word_sequences_comprehensive(word)
            
            # Статистика по длине слова
            total_stats['word_length_stats'][len(word)] += 1
            
            # Статистика по покрытию слова
            if analysis['covers_whole_word']:
                total_stats['word_coverage']['words_with_full_coverage'] += 1
            
            # Агрегируем статистику по длинам последовательностей
            for seq_len in [2, 3, 4, 5]:
                length_data = analysis['sequences_by_length'][seq_len]
                for comfort_type in ['comfortable', 'partial', 'uncomfortable']:
                    total_stats['by_length'][seq_len][comfort_type] += length_data[comfort_type]
                    total_stats['by_length'][seq_len]['total'] += length_data[comfort_type]
            
            # Агрегируем статистику по рукам
            for hand_type in ['left', 'right', 'both']:
                hand_data = analysis['sequences_by_hand'][hand_type]
                for comfort_type in ['comfortable', 'partial', 'uncomfortable']:
                    total_stats['by_hand'][hand_type][comfort_type] += hand_data[comfort_type]
                    total_stats['by_hand'][hand_type]['total'] += hand_data[comfort_type]
            
            # Собираем частоты последовательностей
            for seq, freq in analysis['sequence_frequencies'].items():
                total_stats['sequence_frequencies'][seq] += freq
            
            # Собираем примеры для каждого типа удобства
            for seq_len in [2, 3, 4, 5]:
                for seq_analysis in analysis['sequences_by_length'][seq_len]['details']:
                    comfort_type = seq_analysis['comfort']
                    if len(total_stats['comfort_examples'][comfort_type]) < 10:  # Сохраняем до 10 примеров каждого типа
                        total_stats['comfort_examples'][comfort_type].append(seq_analysis)
        
        # Рассчитываем проценты
        for seq_len in [2, 3, 4, 5]:
            total = total_stats['by_length'][seq_len]['total']
            if total > 0:
                for comfort_type in ['comfortable', 'partial', 'uncomfortable']:
                    count = total_stats['by_length'][seq_len][comfort_type]
                    total_stats['by_length'][seq_len][f'{comfort_type}_percent'] = (count / total) * 100
        
        for hand_type in ['left', 'right', 'both']:
            total = total_stats['by_hand'][hand_type]['total']
            if total > 0:
                for comfort_type in ['comfortable', 'partial', 'uncomfortable']:
                    count = total_stats['by_hand'][hand_type][comfort_type]
                    total_stats['by_hand'][hand_type][f'{comfort_type}_percent'] = (count / total) * 100
        
        # Сортируем последовательности по частоте
        total_stats['sequence_frequencies'] = dict(
            sorted(total_stats['sequence_frequencies'].items(), 
                  key=lambda x: x[1], reverse=True)
        )
        
        # Рассчитываем общую удобность
        total_comfortable = sum(total_stats['by_length'][l]['comfortable'] for l in [2, 3, 4, 5])
        total_sequences = sum(total_stats['by_length'][l]['total'] for l in [2, 3, 4, 5])
        
        total_stats['overall_comfort'] = {
            'comfortable': total_comfortable,
            'total_sequences': total_sequences,
            'comfort_percent': (total_comfortable / total_sequences * 100) if total_sequences > 0 else 0
        }
        
        return total_stats
    
    def prepare_plot_data(self, comprehensive_stats: Dict[str, Any]) -> Dict[str, Any]:
        """
        Подготавливает данные в формате для построения графиков
        """
        plot_data = {
            # Данные для гистограмм по длинам последовательностей
            'by_length': {
                'lengths': ['2 символа', '3 символа', '4 символа', '5 символов'],
                'comfortable': [],
                'partial': [],
                'uncomfortable': [],
                'total_sequences': [],
                'comfortable_percent': [],
                'uncomfortable_percent': []
            },
            
            # Данные для гистограмм по рукам
            'by_hand': {
                'hands': ['Левая рука', 'Правая рука', 'Обе руки'],
                'comfortable': [],
                'partial': [],
                'uncomfortable': [],
                'total_sequences': [],
                'comfortable_percent': [],
                'uncomfortable_percent': []
            },
            
            # Данные для анализа покрытия слов
            'word_coverage': {
                'words_with_full_coverage': comprehensive_stats['word_coverage']['words_with_full_coverage'],
                'total_words': comprehensive_stats['word_coverage']['total_words'],
                'coverage_percent': (comprehensive_stats['word_coverage']['words_with_full_coverage'] / 
                                   comprehensive_stats['word_coverage']['total_words'] * 100) 
                                   if comprehensive_stats['word_coverage']['total_words'] > 0 else 0
            },
            
            # Топ последовательностей для детального анализа
            'top_sequences': {
                'most_frequent': list(comprehensive_stats['sequence_frequencies'].items())[:50],
                'most_comfortable': [],
                'most_uncomfortable': []
            },
            
            # Примеры для легенды графиков
            'examples': comprehensive_stats['comfort_examples'],
            
            # Общая статистика
            'overall': {
                'comfort_percent': comprehensive_stats['overall_comfort']['comfort_percent'],
                'total_sequences': comprehensive_stats['overall_comfort']['total_sequences'],
                'total_words': comprehensive_stats['word_coverage']['total_words']
            }
        }
        
        # Заполняем данные по длинам
        for length in [2, 3, 4, 5]:
            data = comprehensive_stats['by_length'][length]
            plot_data['by_length']['comfortable'].append(data['comfortable'])
            plot_data['by_length']['partial'].append(data['partial'])
            plot_data['by_length']['uncomfortable'].append(data['uncomfortable'])
            plot_data['by_length']['total_sequences'].append(data['total'])
            plot_data['by_length']['comfortable_percent'].append(data.get('comfortable_percent', 0))
            plot_data['by_length']['uncomfortable_percent'].append(data.get('uncomfortable_percent', 0))
        
        # Заполняем данные по рукам
        for hand_type, hand_name in [('left', 'Левая рука'), ('right', 'Правая рука'), ('both', 'Обе руки')]:
            data = comprehensive_stats['by_hand'][hand_type]
            plot_data['by_hand']['comfortable'].append(data['comfortable'])
            plot_data['by_hand']['partial'].append(data['partial'])
            plot_data['by_hand']['uncomfortable'].append(data['uncomfortable'])
            plot_data['by_hand']['total_sequences'].append(data['total'])
            plot_data['by_hand']['comfortable_percent'].append(data.get('comfortable_percent', 0))
            plot_data['by_hand']['uncomfortable_percent'].append(data.get('uncomfortable_percent', 0))
        
        return plot_data


# Функции для работы с файлами (оставляем без изменений)
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
                                   max_samples: int = 10000) -> Dict[str, Any]:
    """
    Анализирует удобность раскладки из файла с новыми требованиями
    """
    analyzer = LayoutAnalyzer(layout_config)
    
    if file_type == 'words':
        total_words = count_lines_in_file(file_path, encoding)
        
        # Собираем слова для анализа (ограничиваем размер для производительности)
        words_for_analysis = []
        word_generator = read_words_by_lines(file_path, batch_size, encoding)
        
        processed_words = 0
        pbar = tqdm(total=min(total_words, max_samples), desc="Сбор слов для анализа")
        
        try:
            for batch in word_generator:
                for word in batch:
                    if len(words_for_analysis) < max_samples:
                        words_for_analysis.append(word)
                        pbar.update(1)
                    processed_words += 1
                    
                    if len(words_for_analysis) >= max_samples:
                        break
                if len(words_for_analysis) >= max_samples:
                    break
        finally:
            pbar.close()
        
        print(f"Проанализировано слов: {len(words_for_analysis):,} из {processed_words:,}")
        
        # Выполняем комплексный анализ
        comprehensive_stats = analyzer.calculate_comprehensive_analysis(words_for_analysis)
        
        # Подготавливаем данные для графиков
        plot_data = analyzer.prepare_plot_data(comprehensive_stats)
        
        # Формируем итоговый результат
        result = {
            'total_words_processed': processed_words,
            'words_analyzed': len(words_for_analysis),
            'overall_comfort_score': comprehensive_stats['overall_comfort']['comfort_percent'],
            'comprehensive_stats': comprehensive_stats,
            'plot_data': plot_data
        }
        
        return result
    
    else:
        raise ValueError("Поддерживается только file_type='words'")

def print_analysis_summary(result):
    """
    Выводит сводку анализа для проверки
    """
    plot_data = result['plot_data']
    
    print("=" * 80)
    print("СВОДКА АНАЛИЗА ДЛЯ ГРАФИКОВ")
    print("=" * 80)
    
    print(f"\n📊 ОБЩАЯ СТАТИСТИКА:")
    print(f"  • Обработано слов: {result['total_words_processed']:,}")
    print(f"  • Проанализировано слов: {result['words_analyzed']:,}")
    print(f"  • Общая удобность: {result['overall_comfort_score']:.1f}%")
    print(f"  • Всего последовательностей: {plot_data['overall']['total_sequences']:,}")
    
    print(f"\n📏 ГИСТОГРАММЫ ПО ДЛИНАМ ПОСЛЕДОВАТЕЛЬНОСТЕЙ:")
    for i, length in enumerate(plot_data['by_length']['lengths']):
        print(f"  • {length}:")
        print(f"      Удобные: {plot_data['by_length']['comfortable'][i]:,} ({plot_data['by_length']['comfortable_percent'][i]:.1f}%)")
        print(f"      Частично удобные: {plot_data['by_length']['partial'][i]:,}")
        print(f"      Неудобные: {plot_data['by_length']['uncomfortable'][i]:,} ({plot_data['by_length']['uncomfortable_percent'][i]:.1f}%)")
        print(f"      Всего: {plot_data['by_length']['total_sequences'][i]:,}")
    
    print(f"\n👐 ГИСТОГРАММЫ ПО РУКАМ:")
    for i, hand in enumerate(plot_data['by_hand']['hands']):
        print(f"  • {hand}:")
        print(f"      Удобные: {plot_data['by_hand']['comfortable'][i]:,} ({plot_data['by_hand']['comfortable_percent'][i]:.1f}%)")
        print(f"      Частично удобные: {plot_data['by_hand']['partial'][i]:,}")
        print(f"      Неудобные: {plot_data['by_hand']['uncomfortable'][i]:,} ({plot_data['by_hand']['uncomfortable_percent'][i]:.1f}%)")
        print(f"      Всего: {plot_data['by_hand']['total_sequences'][i]:,}")
    
    print(f"\n📝 ПОКРЫТИЕ СЛОВ:")
    print(f"  • Слова полностью покрытые последовательностями: {plot_data['word_coverage']['words_with_full_coverage']:,}")
    print(f"  • Всего слов: {plot_data['word_coverage']['total_words']:,}")
    print(f"  • Процент покрытия: {plot_data['word_coverage']['coverage_percent']:.1f}%")
    
    print(f"\n🏆 ТОП-5 САМЫХ ЧАСТЫХ ПОСЛЕДОВАТЕЛЬНОСТЕЙ:")
    for i, (seq, freq) in enumerate(plot_data['top_sequences']['most_frequent'][:5], 1):
        print(f"  {i}. '{seq}': {freq:,} раз")
    
    print(f"\n✅ ПРИМЕРЫ УДОБНЫХ ПОСЛЕДОВАТЕЛЬНОСТЕЙ:")
    for example in plot_data['examples']['comfortable'][:3]:
        print(f"  • '{example['sequence']}' ({example['length']} символа, {example.get('hand_type', 'unknown')})")
    
    print(f"\n❌ ПРИМЕРЫ НЕУДОБНЫХ ПОСЛЕДОВАТЕЛЬНОСТЕЙ:")
    for example in plot_data['examples']['uncomfortable'][:3]:
        print(f"  • '{example['sequence']}' ({example['length']} символа, {example.get('hand_type', 'unknown')}) - {example.get('reason', 'unknown')}")
    
    print("\n" + "=" * 80)
    print("ДАННЫЕ ДЛЯ ГРАФИКОВ ПОДГОТОВЛЕНЫ!")
    print("=" * 80)

# Сохранение результатов в файл
def save_analysis_results(result, output_file: str = "layout_analysis_results_zubachev.json"):
    """Сохраняет результаты анализа в JSON файл"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2, default=str)
    print(f"💾 Результаты сохранены в: {output_file}")

# Пример использования
if __name__ == "__main__":
    # Загрузка раскладки
    layout_config = load_layout_from_json("/Users/evgenii/Develop/py_proj/tr/KVA/example_layouts/zubachew_1.json")
    
    # Анализ файла
    print("Анализ файла со списком слов:")
    result = analyze_layout_comfort_from_file(
        layout_config, 
        "/Users/evgenii/Develop/py_proj/tr/KVA/1grams-3.txt", 
        file_type='words',
        batch_size=1000,
        max_samples=1000000
    )
    
    # Выводим сводку
    print_analysis_summary(result)
    
    # Сохраняем полные результаты
    save_analysis_results(result)