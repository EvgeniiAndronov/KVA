import os
import unittest
import sys
sys.path.append('../../scan_module')
from read_files import get_words_from_file_stream

class TestGetWordsFromFileStream(unittest.TestCase):
    
    def setUp(self):
        self.large_file = "large_test.txt"
        with open(self.large_file, "w", encoding="utf-8") as f:
            for i in range(1500):
                f.write(f"word{i}\n")
    
    def tearDown(self):
        if os.path.exists(self.large_file):
            os.remove(self.large_file)
    
    def test_stream_batch_processing(self):
        batches = list(get_words_from_file_stream(self.large_file, batch_size=500))
        self.assertEqual(len(batches), 3)
        self.assertEqual(len(batches[0]), 500)
        self.assertEqual(len(batches[1]), 500)
        self.assertEqual(len(batches[2]), 500)
    
    def test_stream_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            next(get_words_from_file_stream("nonexistent.txt"))
    
    def test_stream_custom_batch_size(self):
        batches = list(get_words_from_file_stream(self.large_file, batch_size=300))
        self.assertEqual(len(batches), 5)

if __name__ == '__main__':
    unittest.main()