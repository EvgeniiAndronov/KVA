#!/usr/bin/env python3
"""
Скрипт для проверки целостности проекта KVA
"""
import os
import sys
import importlib.util

def check_file_exists(filepath):
    """Проверяет существование файла"""
    if os.path.exists(filepath):
        print(f"✅ {filepath}")
        return True
    else:
        print(f"❌ {filepath} - НЕ НАЙДЕН")
        return False

def check_python_syntax(filepath):
    """Проверяет синтаксис Python файла"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            compile(f.read(), filepath, 'exec')
        print(f"✅ {filepath} - синтаксис OK")
        return True
    except SyntaxError as e:
        print(f"❌ {filepath} - СИНТАКСИЧЕСКАЯ ОШИБКА: {e}")
        return False
    except Exception as e:
        print(f"⚠️  {filepath} - ОШИБКА: {e}")
        return False

def check_imports():
    """Проверяет все импорты"""
    print("\n🔍 ПРОВЕРКА ИМПОРТОВ:")
    
    modules_to_check = [
        'database_module.db_init',
        'database_module.database',
        'scan_module.read_files',
        'scan_module.read_layout',
        'processing_module.calculate_data',
        'data_module.make_export_file',
        'data_module.make_export_plot',
        'output_data.console_strings'
    ]
    
    all_good = True
    for module in modules_to_check:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module} - ОШИБКА ИМПОРТА: {e}")
            all_good = False
        except Exception as e:
            print(f"⚠️  {module} - ОШИБКА: {e}")
            all_good = False
    
    return all_good

def main():
    print("🔍 ПРОВЕРКА ПРОЕКТА KVA")
    print("=" * 50)
    
    # Проверяем основные файлы
    print("\n📁 ПРОВЕРКА ФАЙЛОВ:")
    files_to_check = [
        'main.py',
        'database_module/db_init.py',
        'database_module/database.py',
        'scan_module/read_files.py',
        'scan_module/read_layout.py',
        'processing_module/calculate_data.py',
        'data_module/make_export_file.py',
        'data_module/make_export_plot.py',
        'output_data/console_strings.py',
        'requirements.txt',
        'FEATURES_README.md'
    ]
    
    files_ok = all(check_file_exists(f) for f in files_to_check)
    
    # Проверяем синтаксис Python файлов
    print("\n🐍 ПРОВЕРКА СИНТАКСИСА:")
    python_files = [f for f in files_to_check if f.endswith('.py')]
    syntax_ok = all(check_python_syntax(f) for f in python_files)
    
    # Проверяем импорты
    imports_ok = check_imports()
    
    # Проверяем директории
    print("\n📂 ПРОВЕРКА ДИРЕКТОРИЙ:")
    dirs_to_check = [
        'database_module',
        'scan_module', 
        'processing_module',
        'data_module',
        'output_data',
        'example_layouts',
        'reports'
    ]
    
    dirs_ok = all(check_file_exists(d) for d in dirs_to_check)
    
    # Итоговый результат
    print("\n" + "=" * 50)
    if files_ok and syntax_ok and imports_ok and dirs_ok:
        print("🎉 ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ УСПЕШНО!")
        print("✅ Проект готов к использованию")
        return 0
    else:
        print("❌ ОБНАРУЖЕНЫ ПРОБЛЕМЫ:")
        if not files_ok:
            print("  - Отсутствуют некоторые файлы")
        if not syntax_ok:
            print("  - Синтаксические ошибки в Python файлах")
        if not imports_ok:
            print("  - Проблемы с импортами")
        if not dirs_ok:
            print("  - Отсутствуют некоторые директории")
        return 1

if __name__ == "__main__":
    sys.exit(main())