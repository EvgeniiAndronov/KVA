def get_words_from_file(filename: str) -> list:
    """
    Считывает построчно из файла слова и преобразует
    их в список для удобной обработки.
    """
    all_words_from_file = []
    with open(f"{filename}", "r") as file:
        lines = file.readlines()

    for line in lines:
        all_words_from_file.append(line.strip())

    return all_words_from_file


def text_from_file():
    pass
