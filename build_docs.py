#!/usr/bin/env python3
"""
Скрипт для сборки документации Sphinx (Windows-совместимый)
"""

import os
import sys
import subprocess
from pathlib import Path

def is_windows():
    """Проверяет, работает ли на Windows"""
    return os.name == 'nt'

def build_docs():
    """Собирает документацию Sphinx"""
    
    # Переходим в папку docs
    docs_dir = Path(__file__).parent / "docs"
    if not docs_dir.exists():
        print("❌ Папка docs не найдена!")
        return False
    
    os.chdir(docs_dir)
    
    print("🔄 Очистка предыдущей сборки...")
    try:
        if is_windows():
            # Для Windows: используем sphinx-build вместо make
            if (docs_dir / "build").exists():
                subprocess.run(["rmdir", "/s", "/q", "build"], shell=True, check=True)
            print("✅ Очистка завершена")
        else:
            # Для Linux/Mac
            subprocess.run(["make", "clean"], check=True)
            print("✅ Очистка завершена")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"⚠️  Ошибка очистки: {e}")
    
    print("📚 Сборка HTML документации...")
    try:
        if is_windows():
            # Для Windows: используем sphinx-build напрямую
            result = subprocess.run([
                "sphinx-build", "-b", "html", "source", "build"
            ], check=True, capture_output=True, text=True)
        else:
            # Для Linux/Mac
            result = subprocess.run(["make", "html"], check=True, capture_output=True, text=True)
        
        print("✅ Документация успешно собрана!")
        
        # Показываем путь к документации
        build_path = docs_dir / "build" / "html" / "index.html"
        print(f"📖 Документация доступна по адресу: file://{build_path.absolute()}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print("❌ Ошибка сборки документации:")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False
    except FileNotFoundError as e:
        print("❌ Команда не найдена. Убедитесь, что Sphinx установлен:")
        print("Установите: pip install sphinx sphinx-rtd-theme")
        return False

def main():
    """Главная функция"""
    print("🐭 TEAM RATS - Сборка документации KVA")
    print("=" * 50)
    print(f"🏃‍♂️  Платформа: {'Windows' if is_windows() else 'Linux/Mac'}")
    
    # Проверяем наличие Sphinx
    try:
        subprocess.run(["sphinx-build", "--version"], check=True, capture_output=True)
        print("✅ Sphinx обнаружен")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Sphinx не установлен!")
        print("Установите его командой: pip install sphinx sphinx-rtd-theme")
        return 1
    
    if build_docs():
        print("\n🎉 Сборка документации завершена успешно!")
        return 0
    else:
        print("\n💥 Ошибка при сборке документации!")
        return 1

if __name__ == "__main__":
    sys.exit(main())