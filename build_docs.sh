#!/bin/bash
# Скрипт сборки документации для Unix-систем (Linux/macOS)

echo "🐭 TEAM RATS - Сборка документации KVA (Unix)"
echo "=============================================="

# Проверяем наличие Python
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "❌ Python не найден! Установите Python"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "🐍 Используем: $PYTHON_CMD"

# Запускаем Python скрипт
$PYTHON_CMD build_docs.py

# Показываем результат
if [ $? -eq 0 ]; then
    echo ""
    echo "💡 Для открытия документации:"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "   open docs/build/html/index.html"
    else
        echo "   xdg-open docs/build/html/index.html"
    fi
fi