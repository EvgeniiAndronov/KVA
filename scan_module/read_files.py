import os
from typing import Generator, List


def get_file_size_mb(filename: str) -> float:
    """Возвращает размер файла в мегабайтах"""
    try:
        size_bytes = os.path.getsize(filename)
        return size_bytes / (1024 * 1024)
    except OSError:
        return 0


def get_words_from_file(filename: str) -> list:
    """
    Считывает построчно из файла слова и преобразует
    их в список для удобной обработки.
    ВНИМАНИЕ: Используйте только для небольших файлов!
    """
    file_size = get_file_size_mb(filename)
    if file_size > 50:  # Предупреждение для файлов больше 50MB
        raise ValueError(f"Файл слишком большой ({file_size:.1f}MB). Используйте get_words_from_file_stream()")
    
    all_words_from_file = []
    try:
        with open(filename, "r", encoding='utf-8') as file:
            for line in file:
                word = line.strip()
                if word:  # Пропускаем пустые строки
                    all_words_from_file.append(word)
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {filename}")
    except UnicodeDecodeError:
        # Пробуем другую кодировку
        with open(filename, "r", encoding='latin-1') as file:
            for line in file:
                word = line.strip()
                if word:
                    all_words_from_file.append(word)

    return all_words_from_file


def get_words_from_file_stream(filename: str, batch_size: int = 1000) -> Generator[List[str], None, None]:
    """
    Генератор для потоковой обработки больших файлов.
    Возвращает батчи слов для эффективной обработки.
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Файл не найден: {filename}")
    
    try:
        with open(filename, "r", encoding='utf-8') as file:
            batch = []
            for line in file:
                word = line.strip()
                if word:  # Пропускаем пустые строки
                    batch.append(word)
                    if len(batch) >= batch_size:
                        yield batch
                        batch = []
            if batch:  # Возвращаем последний неполный батч
                yield batch
    except UnicodeDecodeError:
        # Пробуем другую кодировку
        with open(filename, "r", encoding='latin-1') as file:
            batch = []
            for line in file:
                word = line.strip()
                if word:
                    batch.append(word)
                    if len(batch) >= batch_size:
                        yield batch
                        batch = []
            if batch:
                yield batch


def count_lines_in_file(filename: str) -> int:
    """Подсчитывает количество непустых строк в файле"""
    try:
        with open(filename, "r", encoding='utf-8') as file:
            return sum(1 for line in file if line.strip())
    except UnicodeDecodeError:
        with open(filename, "r", encoding='latin-1') as file:
            return sum(1 for line in file if line.strip())


def get_text_from_file(filename: str) -> str:
    """
    Считывает весь текст из файла как единую строку.
    ВНИМАНИЕ: Используйте только для небольших файлов!
    """
    file_size = get_file_size_mb(filename)
    if file_size > 50:
        raise ValueError(f"Файл слишком большой ({file_size:.1f}MB). Используйте get_text_from_file_stream()")
    
    try:
        with open(filename, "r", encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {filename}")
    except UnicodeDecodeError:
        # Пробуем другую кодировку
        with open(filename, "r", encoding='latin-1') as file:
            return file.read()


def get_text_from_file_stream(filename: str, chunk_size: int = 8192) -> Generator[str, None, None]:
    """
    Генератор для потокового чтения больших текстовых файлов.
    Возвращает чанки текста для эффективной обработки.
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Файл не найден: {filename}")
    
    try:
        with open(filename, "r", encoding='utf-8') as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                yield chunk
    except UnicodeDecodeError:
        # Пробуем другую кодировку
        with open(filename, "r", encoding='latin-1') as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                yield chunk


def count_characters_in_file(filename: str) -> int:
    """Подсчитывает количество символов в файле"""
    try:
        with open(filename, "r", encoding='utf-8') as file:
            return sum(len(chunk) for chunk in iter(lambda: file.read(8192), ''))
    except UnicodeDecodeError:
        with open(filename, "r", encoding='latin-1') as file:
            return sum(len(chunk) for chunk in iter(lambda: file.read(8192), ''))
