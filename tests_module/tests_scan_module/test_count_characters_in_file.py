import os
import unittest

class TestCountCharactersInFile(unittest.TestCase):
    
    def setUp(self):
        """
        Создает имя тестового файла перед 
        каждым тестом
        """
        self.test_file = "char_test.txt"
    
    def tearDown(self):
        """
        Удаляет тестовый файл после каждого 
        теста
        """
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_count_characters_ascii(self):
        """
        Тест, который проверяет подсчет 
        символов в файле с ASCII текстом
        """
        from scan_module.read_files import count_characters_in_file
        content = "abcdefghij"
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write(content)
        
        count = count_characters_in_file(self.test_file)
        self.assertEqual(count, len(content))
    
    def test_count_characters_unicode(self):
        """
        Тест, который проверяет подсчет 
        символов в файле с Unicode текстом
        """
        from scan_module.read_files import count_characters_in_file
        content = "абвгд€¥£"
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write(content)
        
        count = count_characters_in_file(self.test_file)
        self.assertEqual(count, len(content))
    
    def test_count_characters_empty_file(self):
        """
        Тест, который проверяет подсчет 
        символов в пустом файле
        """
        from scan_module.read_files import count_characters_in_file
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("")
        
        count = count_characters_in_file(self.test_file)
        self.assertEqual(count, 0)

if __name__ == '__main__':
    unittest.main()