import os
import unittest

class TestGetWordsFromFile(unittest.TestCase):
    
    def setUp(self):
        """
        Создает тестовый файл со словами 
        перед каждым тестом
        """
        self.small_file = "small_test.txt"
        with open(self.small_file, "w", encoding="utf-8") as f:
            f.write("word1\nword2\nword3\n")
    
    def tearDown(self):
        """
        Удаляет тестовый файл после каждого 
        теста
        """
        if os.path.exists(self.small_file):
            os.remove(self.small_file)
    
    def test_get_words_normal_case(self):
        """
        Тест, который проверяет чтение слов 
        из файла в нормальном случае
        """
        from scan_module.read_files import get_words_from_file
        words = get_words_from_file(self.small_file)
        self.assertEqual(words, ["word1", "word2", "word3"])
    
    def test_get_words_with_empty_lines(self):
        """
        Тест, который проверяет чтение слов 
        из файла с пустыми строками (должны 
        игнорироваться)
        """
        from scan_module.read_files import get_words_from_file
        with open(self.small_file, "w", encoding="utf-8") as f:
            f.write("word1\n\nword2\n\nword3\n")
        
        words = get_words_from_file(self.small_file)
        self.assertEqual(words, ["word1", "word2", "word3"])
    
    def test_get_words_file_not_found(self):
        """
        Тест, который проверяет обработку 
        ошибки отсутствия файла
        """
        from scan_module.read_files import get_words_from_file
        with self.assertRaises(FileNotFoundError):
            get_words_from_file("nonexistent.txt")

if __name__ == '__main__':
    unittest.main()