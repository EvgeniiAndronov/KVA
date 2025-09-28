import os
import unittest

class TestCountLinesInFile(unittest.TestCase):
    
    def setUp(self):
        """
        Создает имя тестового файла перед 
        каждым тестом
        """
        self.test_file = "line_test.txt"
    
    def tearDown(self):
        """
        Удаляет тестовый файл после каждого 
        теста
        """
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_count_lines_with_content(self):
        """
        Тест, который проверяет подсчет строк 
        в файле с содержимым
        """
        from scan_module.read_files import count_lines_in_file
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("line1\nline2\nline3\n")
        
        count = count_lines_in_file(self.test_file)
        self.assertEqual(count, 3)
    
    def test_count_lines_empty_file(self):
        """
        Тест, который проверяет подсчет строк 
        в пустом файле
        """
        from scan_module.read_files import count_lines_in_file
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("")
        
        count = count_lines_in_file(self.test_file)
        self.assertEqual(count, 0)
    
    def test_count_lines_with_blank_lines(self):
        """
        Тест, который проверяет подсчет строк в 
        файле с пустыми строками (должны 
        игнорироваться)
        """
        from scan_module.read_files import count_lines_in_file
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("line1\n\nline2\n  \nline3\n")
        
        count = count_lines_in_file(self.test_file)
        self.assertEqual(count, 3)

if __name__ == '__main__':
    unittest.main()