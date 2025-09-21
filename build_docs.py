#!/usr/bin/env python3
"""
Скрипт для сборки документации Sphinx
"""

import os
import sys
import subprocess
from pathlib import Path

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
        subprocess.run(["make", "clean"], check=True)
        print("✅ Очистка завершена")
    except subprocess.CalledProcessError:
        print("⚠️  Ошибка очистки (возможно, папка build не существует)")
    
    print("📚 Сборка HTML документации...")
    try:
        result = subprocess.run(["make", "html"], check=True, capture_output=True, text=True)
        print("✅ Документация успешно собрана!")
        
        # Показываем путь к документации
        build_path = docs_dir / "build" / "html" / "index.html"
        print(f"📖 Документация доступна по адресу: file://{build_path.absolute()}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print("❌ Ошибка сборки документации:")
        print(e.stdout)
        print(e.stderr)
        return False

def main():
    """Главная функция"""
    print("🐭 TEAM RATS - Сборка документации KVA")
    print("=" * 50)
    
    # Проверяем наличие Sphinx
    try:
        subprocess.run(["sphinx-build", "--version"], check=True, capture_output=True)
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