from enum import Enum
from typing import Optional
import sys
from datetime import datetime

from database_module.db_init import init_tables, make_mok_data
from database_module.database import (
    take_lk_from_db, 
    take_all_data_from_lk, 
    take_lk_names_from_lk,
    save_analysis_result,
    get_analysis_history,
    get_analysis_statistics
)
from scan_module.read_files import (
    get_words_from_file, 
    get_words_from_file_stream, 
    get_text_from_file,
    get_text_from_file_stream,
    get_file_size_mb,
    count_lines_in_file,
    count_characters_in_file
)
from processing_module.calculate_data import (
    make_processing, 
    make_processing_stream,
    make_text_processing,
    make_text_processing_stream,
    validate_rules
)
from data_module.make_export_file import create_csv_report, export_unknown_characters_csv
from data_module.make_export_plot import (
    create_analysis_charts, 
    create_history_comparison_chart, 
    create_layouts_comparison_chart
)
from output_data.console_strings import *
from scan_module.read_layout import read_kl


class MenuAction(Enum):
    """Перечисление возможных действий в меню"""
    EXIT = 0
    BACK = -1
    CONTINUE = 1


class MenuSystem:
    """Система меню с улучшенной навигацией"""
    
    def __init__(self):
        self.current_layout = None
        self.current_layout_name = None
    
    def get_user_choice(self, prompt: str = "--> ", min_val: int = 0, max_val: int = None) -> int:
        """Безопасный ввод числа от пользователя с валидацией"""
        while True:
            try:
                choice = int(input(prompt))
                if choice < min_val:
                    print(f"Значение должно быть не меньше {min_val}")
                    continue
                if max_val is not None and choice > max_val:
                    print(f"Значение должно быть не больше {max_val}")
                    continue
                return choice
            except ValueError:
                print(error_input_data)
            except KeyboardInterrupt:
                print("\nВыход из программы...")
                sys.exit(0)
    
    def confirm_action(self, message: str) -> bool:
        """Запрос подтверждения действия"""
        while True:
            response = input(f"{message} (y/n): ").lower().strip()
            if response in ['y', 'yes', 'да', 'д']:
                return True
            elif response in ['n', 'no', 'нет', 'н']:
                return False
            else:
                print("Введите 'y' для подтверждения или 'n' для отмены")
    
    def display_menu_header(self, title: str):
        """Отображение заголовка меню"""
        print("\n" + "="*50)
        print(f" {title}")
        print("="*50)
    
    def main_menu(self) -> MenuAction:
        """Главное меню"""
        self.display_menu_header("ГЛАВНОЕ МЕНЮ")
        print(rat_img_msg)
        print("1) Выбрать раскладку для тестирования")
        print("0) Выход из программы")
        
        choice = self.get_user_choice(max_val=1)
        
        if choice == 0:
            return MenuAction.EXIT
        elif choice == 1:
            return self.layout_selection_menu()
        
        return MenuAction.CONTINUE
    
    def layout_selection_menu(self) -> MenuAction:
        """Меню выбора раскладки"""
        self.display_menu_header("ВЫБОР РАСКЛАДКИ")
        
        layouts = take_lk_names_from_lk()
        if not layouts:
            print("❌ В базе данных нет доступных раскладок")
            input("Нажмите Enter для продолжения...")
            return MenuAction.CONTINUE
        
        print("Доступные раскладки:")
        for i, layout in enumerate(layouts, 1):
            status = "✅ (выбрана)" if self.current_layout_name == layout[0] else ""
            print(f"{i}) {layout[0]} {status}")
        
        print("0) Назад в главное меню")
        
        choice = self.get_user_choice(max_val=len(layouts))
        
        if choice == 0:
            return MenuAction.CONTINUE
        
        selected_layout_name = layouts[choice - 1][0]
        selected_layout = take_lk_from_db(selected_layout_name)
        
        if selected_layout is None:
            print("❌ Ошибка загрузки раскладки из БД")
            input("Нажмите Enter для продолжения...")
            return MenuAction.CONTINUE
        
        try:
            validate_rules(selected_layout)
            self.current_layout = selected_layout
            self.current_layout_name = selected_layout_name
            print(f"✅ Раскладка '{selected_layout_name}' выбрана")
            
            return self.file_processing_menu()
            
        except ValueError as e:
            print(f"❌ Ошибка валидации раскладки: {e}")
            input("Нажмите Enter для продолжения...")
            return MenuAction.CONTINUE
    
    def file_processing_menu(self) -> MenuAction:
        """Меню обработки файлов"""
        if not self.current_layout:
            print("❌ Сначала выберите раскладку")
            return MenuAction.CONTINUE
        
        self.display_menu_header(f"ОБРАБОТКА ФАЙЛОВ - {self.current_layout_name}")
        print("1) Обработать файл со словами (построчно)")
        print("2) Обработать текстовый файл (сплошной текст)")
        print("3) История анализов")
        print("4) Создать графики сравнения")
        print("5) Загрузить раскладку из файла")
        print("6) Сменить раскладку")
        print("0) Назад в главное меню")
        
        choice = self.get_user_choice(max_val=6)
        
        if choice == 0:
            return MenuAction.CONTINUE
        elif choice == 1:
            self.process_word_file()
        elif choice == 2:
            self.process_text_file()
        elif choice == 3:
            self.show_analysis_history()
        elif choice == 4:
            self.create_comparison_charts()
        elif choice == 5:
            self.load_layout_from_file()
        elif choice == 6:
            self.current_layout = None
            self.current_layout_name = None
            return self.layout_selection_menu()
        
        return MenuAction.CONTINUE
    
    def process_word_file(self):
        """Обработка файла со словами"""
        print("\n📁 Обработка файла со словами")
        file_path = input("Введите полный путь к файлу: ").strip()
        
        if not file_path:
            print("❌ Путь к файлу не может быть пустым")
            return
        
        try:
            file_size = get_file_size_mb(file_path)
            print(f"📊 Размер файла: {file_size:.1f} MB")
            
            if file_size > 50:
                if not self.confirm_action(f"⚠️  Файл очень большой ({file_size:.1f}MB). Продолжить?"):
                    print("❌ Обработка отменена")
                    return
            
            if file_size > 10:
                self._process_large_file(file_path, file_size)
            else:
                self._process_small_file(file_path)
                
        except FileNotFoundError:
            print(f"❌ Файл не найден: {file_path}")
        except Exception as e:
            print(f"❌ Ошибка обработки файла: {e}")
        
        input("\nНажмите Enter для продолжения...")
    
    def _process_large_file(self, file_path: str, file_size: float):
        """Обработка большого файла потоково"""
        print(f"🔄 Большой файл ({file_size:.1f}MB). Используем потоковую обработку...")
        
        print("📊 Подсчитываем количество слов...")
        total_words = count_lines_in_file(file_path)
        print(f"📝 Найдено {total_words:,} слов")
        
        if total_words > 1000000:
            if not self.confirm_action(f"⚠️  Файл содержит {total_words:,} слов. Обработка может занять много времени. Продолжить?"):
                print("❌ Обработка отменена")
                return
        
        try:
            word_generator = get_words_from_file_stream(file_path, batch_size=5000)
            result = make_processing_stream(word_generator, self.current_layout, total_words)
            self._display_detailed_results(result, file_path)
            
        except KeyboardInterrupt:
            print("\n❌ Обработка прервана пользователем")
    
    def _process_small_file(self, file_path: str):
        """Обработка небольшого файла"""
        print("📥 Загружаем файл в память...")
        words = get_words_from_file(file_path)
        print(f"📝 Загружено {len(words):,} слов")
        
        result = make_processing(words, self.current_layout)
        self._display_detailed_results(result, file_path)
    
    def _display_detailed_results(self, result: dict, file_path: str):
        """Отображение детальных результатов обработки"""
        print(f"\n{'='*70}")
        print(f"🎯 РЕЗУЛЬТАТЫ АНАЛИЗА РАСКЛАДКИ")
        print(f"{'='*70}")
        print(f"📁 Файл: {file_path}")
        print(f"⌨️  Раскладка: {self.current_layout_name}")
        print(f"{'='*70}")
        
        # Основная статистика
        print(f"📝 Обработано слов: {result['total_words']:,}")
        print(f"🔤 Всего символов: {result['total_characters']:,}")
        print(f"✅ Обработано символов: {result['processed_characters']:,}")
        print(f"❌ Общее количество ошибок: {result['total_errors']:,}")
        
        # Средние значения
        print(f"\n📊 СТАТИСТИКА:")
        print(f"   • Среднее ошибок на слово: {result['avg_errors_per_word']:.2f}")
        print(f"   • Среднее ошибок на символ: {result['avg_errors_per_char']:.4f}")
        
        # Покрытие символов
        if result['total_characters'] > 0:
            coverage = (result['processed_characters'] / result['total_characters']) * 100
            print(f"   • Покрытие раскладкой: {coverage:.1f}%")
        
        # Неизвестные символы
        if result['unknown_characters']:
            print(f"\n⚠️  НЕИЗВЕСТНЫЕ СИМВОЛЫ ({len(result['unknown_characters'])} шт.):")
            unknown_list = sorted(list(result['unknown_characters']))
            # Показываем первые 20 символов
            display_chars = unknown_list[:20]
            print(f"   {', '.join(repr(char) for char in display_chars)}")
            if len(unknown_list) > 20:
                print(f"   ... и еще {len(unknown_list) - 20} символов")
        
        # Оценка качества
        print(f"\n🏆 ОЦЕНКА КАЧЕСТВА:")
        if result['avg_errors_per_word'] < 2:
            print("   ✅ ОТЛИЧНО - Очень низкий уровень ошибок!")
        elif result['avg_errors_per_word'] < 5:
            print("   🟢 ХОРОШО - Приемлемый уровень ошибок")
        elif result['avg_errors_per_word'] < 10:
            print("   🟡 СРЕДНЕ - Есть место для улучшения")
        else:
            print("   🔴 ПЛОХО - Высокий уровень ошибок")
        
        print(f"{'='*70}")
        
        # Предлагаем сохранить результаты
        self._offer_save_and_export(result, file_path)
    
    def process_text_file(self):
        """Обработка текстового файла (сплошной текст)"""
        print("\n📄 Обработка текстового файла")
        file_path = input("Введите полный путь к файлу: ").strip()
        
        if not file_path:
            print("❌ Путь к файлу не может быть пустым")
            return
        
        try:
            file_size = get_file_size_mb(file_path)
            print(f"📊 Размер файла: {file_size:.1f} MB")
            
            if file_size > 50:
                if not self.confirm_action(f"⚠️  Файл очень большой ({file_size:.1f}MB). Продолжить?"):
                    print("❌ Обработка отменена")
                    return
            
            if file_size > 10:
                self._process_large_text_file(file_path, file_size)
            else:
                self._process_small_text_file(file_path)
                
        except FileNotFoundError:
            print(f"❌ Файл не найден: {file_path}")
        except Exception as e:
            print(f"❌ Ошибка обработки файла: {e}")
        
        input("\nНажмите Enter для продолжения...")
    
    def _process_large_text_file(self, file_path: str, file_size: float):
        """Обработка большого текстового файла потоково"""
        print(f"🔄 Большой текстовый файл ({file_size:.1f}MB). Используем потоковую обработку...")
        
        print("📊 Подсчитываем количество символов...")
        total_chars = count_characters_in_file(file_path)
        print(f"📝 Найдено {total_chars:,} символов")
        
        if total_chars > 10000000:  # 10 миллионов символов
            if not self.confirm_action(f"⚠️  Файл содержит {total_chars:,} символов. Обработка может занять много времени. Продолжить?"):
                print("❌ Обработка отменена")
                return
        
        try:
            text_generator = get_text_from_file_stream(file_path, chunk_size=16384)
            result = make_text_processing_stream(text_generator, self.current_layout, total_chars)
            self._display_detailed_results(result, file_path)
            
        except KeyboardInterrupt:
            print("\n❌ Обработка прервана пользователем")
    
    def _process_small_text_file(self, file_path: str):
        """Обработка небольшого текстового файла"""
        print("📥 Загружаем текст в память...")
        text = get_text_from_file(file_path)
        print(f"📝 Загружено {len(text):,} символов")
        
        result = make_text_processing(text, self.current_layout)
        self._display_detailed_results(result, file_path)
    
    def _offer_save_and_export(self, result: dict, file_path: str):
        """Предлагает сохранить результаты и экспортировать"""
        print(f"\n💾 СОХРАНЕНИЕ И ЭКСПОРТ РЕЗУЛЬТАТОВ")
        print("1) Сохранить в базу данных")
        print("2) Экспортировать в CSV")
        print("3) Создать графики анализа")
        print("4) Экспортировать неизвестные символы в CSV")
        print("5) Все вышеперечисленное")
        print("0) Пропустить")
        
        choice = self.get_user_choice(max_val=5)
        
        if choice == 0:
            return
        
        analysis_type = result.get('text_type', 'words')
        
        if choice in [1, 5]:
            try:
                record_id = save_analysis_result(
                    self.current_layout_name, 
                    result, 
                    file_path, 
                    analysis_type
                )
                print(f"✅ Результаты сохранены в БД (ID: {record_id})")
            except Exception as e:
                print(f"❌ Ошибка сохранения в БД: {e}")
        
        if choice in [2, 5]:
            try:
                csv_path = create_csv_report(result, file_path, self.current_layout_name)
                print(f"✅ CSV отчет создан: {csv_path}")
            except Exception as e:
                print(f"❌ Ошибка создания CSV: {e}")
        
        if choice in [3, 5]:
            try:
                chart_paths = create_analysis_charts(result, self.current_layout_name, file_path)
                if chart_paths:
                    print(f"✅ Созданы графики:")
                    for path in chart_paths:
                        print(f"   📊 {path}")
                else:
                    print("⚠️  Не удалось создать графики")
            except Exception as e:
                print(f"❌ Ошибка создания графиков: {e}")
        
        if choice in [4, 5] and result['unknown_characters']:
            try:
                chars_csv_path = export_unknown_characters_csv(
                    result['unknown_characters'], 
                    self.current_layout_name
                )
                print(f"✅ CSV с неизвестными символами создан: {chars_csv_path}")
            except Exception as e:
                print(f"❌ Ошибка экспорта символов: {e}")
    
    def show_analysis_history(self):
        """Показывает историю анализов"""
        self.display_menu_header(f"ИСТОРИЯ АНАЛИЗОВ - {self.current_layout_name}")
        
        try:
            # Получаем статистику
            stats = get_analysis_statistics(self.current_layout_name)
            print(f"📊 СТАТИСТИКА:")
            print(f"   • Всего тестов: {stats['total_tests']}")
            if stats['total_tests'] > 0:
                print(f"   • Среднее ошибок: {stats['avg_errors']:.2f}")
                print(f"   • Минимум ошибок: {stats['min_errors']}")
                print(f"   • Максимум ошибок: {stats['max_errors']}")
            
            # Получаем историю
            history = get_analysis_history(self.current_layout_name, limit=20)
            
            if not history:
                print("\n❌ История анализов пуста")
                input("Нажмите Enter для продолжения...")
                return
            
            print(f"\n📋 ПОСЛЕДНИЕ {len(history)} АНАЛИЗОВ:")
            print(f"{'ID':<5} {'Ошибки':<10} {'Тип':<15} {'Файл'}")
            print("-" * 70)
            
            for record in history:
                record_id, layout_name, errors, test_type = record
                
                # Парсим тип теста
                parts = test_type.split('|')
                analysis_type = parts[0] if len(parts) > 0 else 'unknown'
                file_name = parts[1].split('/')[-1] if len(parts) > 1 else 'unknown'
                
                print(f"{record_id:<5} {errors:<10} {analysis_type:<15} {file_name[:40]}")
            
        except Exception as e:
            print(f"❌ Ошибка получения истории: {e}")
        
        input("\nНажмите Enter для продолжения...")
    
    def create_comparison_charts(self):
        """Создает сравнительные графики"""
        self.display_menu_header("СОЗДАНИЕ ГРАФИКОВ")
        print("1) График истории анализов текущей раскладки")
        print("2) Сравнение всех раскладок")
        print("0) Назад")
        
        choice = self.get_user_choice(max_val=2)
        
        if choice == 0:
            return
        
        try:
            if choice == 1:
                chart_path = create_history_comparison_chart(self.current_layout_name)
                if chart_path:
                    print(f"✅ График истории создан: {chart_path}")
                else:
                    print("⚠️  Недостаточно данных для создания графика истории")
            
            elif choice == 2:
                chart_path = create_layouts_comparison_chart()
                if chart_path:
                    print(f"✅ Сравнительный график создан: {chart_path}")
                else:
                    print("⚠️  Недостаточно данных для сравнения раскладок")
        
        except Exception as e:
            print(f"❌ Ошибка создания графика: {e}")
        
        input("\nНажмите Enter для продолжения...")
    
    def load_layout_from_file(self):
        """Загружает раскладку из файла"""
        self.display_menu_header("ЗАГРУЗКА РАСКЛАДКИ ИЗ ФАЙЛА")
        
        file_path = input("Введите путь к файлу раскладки: ").strip()
        if not file_path:
            print("❌ Путь к файлу не может быть пустым")
            input("Нажмите Enter для продолжения...")
            return
        
        try:
            layout = read_kl(file_path)
            if layout is None:
                print("❌ Не удалось загрузить раскладку из файла")
                input("Нажмите Enter для продолжения...")
                return
            
            # Валидируем раскладку
            from scan_module.read_layout import validate_layout
            is_valid, errors = validate_layout(layout)
            
            if not is_valid:
                print("⚠️  Обнаружены проблемы с раскладкой:")
                for error in errors[:5]:  # Показываем первые 5 ошибок
                    print(f"   • {error}")
                if len(errors) > 5:
                    print(f"   ... и еще {len(errors) - 5} ошибок")
                
                if not self.confirm_action("Продолжить с этой раскладкой?"):
                    return
            
            # Предлагаем сохранить в БД
            layout_name = input("Введите название для раскладки: ").strip()
            if not layout_name:
                layout_name = f"imported_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            if self.confirm_action(f"Сохранить раскладку '{layout_name}' в базу данных?"):
                self._save_layout_to_db(layout, layout_name)
            
            # Устанавливаем как текущую раскладку
            self.current_layout = layout
            self.current_layout_name = layout_name
            
            print(f"✅ Раскладка '{layout_name}' загружена и установлена как текущая")
            print(f"📊 Содержит {len(layout)} символов")
            
        except Exception as e:
            print(f"❌ Ошибка загрузки раскладки: {e}")
        
        input("\nНажмите Enter для продолжения...")
    
    def _save_layout_to_db(self, layout: dict, layout_name: str):
        """Сохраняет раскладку в базу данных"""
        try:
            import sqlite3
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            
            # Удаляем старую раскладку с таким же именем
            cursor.execute("DELETE FROM lk WHERE name_lk = ?", (layout_name,))
            
            # Добавляем новую раскладку
            for symbol, error_value in layout.items():
                cursor.execute(
                    "INSERT INTO lk (name_lk, letter, error) VALUES (?, ?, ?)",
                    (layout_name, symbol, error_value)
                )
            
            conn.commit()
            conn.close()
            
            print(f"✅ Раскладка '{layout_name}' сохранена в базу данных")
            
        except Exception as e:
            print(f"❌ Ошибка сохранения раскладки в БД: {e}")
    
    def run(self):
        """Запуск системы меню"""
        print("🐭 Добро пожаловать в TEAM RATS Keyboard Layout Analyzer!")
        
        try:
            while True:
                action = self.main_menu()
                if action == MenuAction.EXIT:
                    break
                    
        except KeyboardInterrupt:
            print("\n👋 До свидания!")
        except Exception as e:
            print(f"💥 Критическая ошибка: {e}")
        
        print("👋 Программа завершена")


def main():
    """
    Главная функция программы
    """
    init_tables()
    make_mok_data("a", "test_en")
    menu_system = MenuSystem()
    menu_system.run()

if __name__ == "__main__":
    main()
