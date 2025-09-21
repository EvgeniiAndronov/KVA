@echo off
REM Скрипт сборки документации для Windows
echo 🐭 TEAM RATS - Сборка документации KVA (Windows)
echo ==================================================

REM Проверяем наличие Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не найден! Установите Python с python.org
    pause
    exit /b 1
)

REM Запускаем Python скрипт
python build_docs.py

REM Пауза для просмотра результата
pause