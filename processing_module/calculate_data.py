def make_processing(wordlist: list, ruls: dict) -> int:
    mistakes = 0
    for word in wordlist:
        for letter in word:
            mistakes += ruls[letter]

    return mistakes