# 🚀 Установка и запуск KVA

## Быстрый старт

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Проверка проекта
```bash
python check_project.py
```

### 3. Запуск программы
```bash
python main.py
```

## Подробная установка

### Требования
- Python 3.8 или выше
- pip (менеджер пакетов Python)

### Установка зависимостей
```bash
# Основные зависимости
pip install matplotlib>=3.5.0
pip install tqdm>=4.64.0
pip install numpy>=1.21.0

# Или все сразу из файла
pip install -r requirements.txt
```

### Проверка установки
```bash
# Проверка импортов
python test_imports.py

# Полная проверка проекта
python check_project.py
```

## Первый запуск

1. **Запустите программу:**
   ```bash
   python main.py
   ```

2. **Выберите раскладку:**
   - В меню выберите "1) Выбрать раскладку для тестирования"
   - Выберите "test_en" (создается автоматически)

3. **Проанализируйте файл:**
   - Выберите "1) Обработать файл со словами"
   - Укажите путь к файлу (например: `test_words.txt`)

4. **Сохраните результаты:**
   - Выберите нужные опции экспорта
   - Графики сохранятся в папку `reports/`

## Примеры файлов

### Тестовые файлы:
- `test_words.txt` - небольшой файл для тестирования
- `rockyou.txt` - большой файл паролей (134MB)

### Примеры раскладок:
- `example_layouts/qwerty_layout.json` - QWERTY в JSON
- `example_layouts/dvorak_layout.csv` - Dvorak в CSV  
- `example_layouts/colemak_layout.txt` - Colemak в TXT

## Структура проекта

```
KVA/
├── main.py                 # 🎯 Главный файл
├── requirements.txt        # 📦 Зависимости
├── check_project.py       # 🔍 Проверка проекта
├── database_module/       # 💾 Работа с БД
├── scan_module/           # 📖 Чтение файлов
├── processing_module/     # ⚙️  Обработка данных
├── data_module/           # 📊 Экспорт и графики
├── example_layouts/       # 📝 Примеры раскладок
└── reports/              # 📈 Отчеты и графики
```

## Возможные проблемы

### Ошибка импорта matplotlib
```bash
# Ubuntu/Debian
sudo apt-get install python3-matplotlib

# macOS
brew install python-tk

# Windows
pip install matplotlib
```

### Ошибка "No module named 'tkinter'"
```bash
# Ubuntu/Debian  
sudo apt-get install python3-tk

# CentOS/RHEL
sudo yum install tkinter
```

### Проблемы с кодировкой
- Убедитесь, что файлы сохранены в UTF-8
- Для Windows может потребоваться указать кодировку

## Получение помощи

1. **Проверьте документацию:** `FEATURES_README.md`
2. **Запустите диагностику:** `python check_project.py`
3. **Проверьте импорты:** `python test_imports.py`

---

*Создано командой TEAM RATS 🐭*