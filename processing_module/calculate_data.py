def make_processing(wordlist: list, ruls: dict) -> int:
    """
    Считает количество ошибок по словарю правил и списку слов.
    """
    mistakes = 0
    for word in wordlist:
        for letter in word:
            mistakes += ruls[letter]

    return mistakes