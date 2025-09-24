import os
import unittest

class TestGetTextFromFileStream(unittest.TestCase):
    
    def setUp(self):
        self.large_file = "large_text.txt"
        self.content = "A" * 10000
        with open(self.large_file, "w", encoding="utf-8") as f:
            f.write(self.content)
    
    def tearDown(self):
        if os.path.exists(self.large_file):
            os.remove(self.large_file)
    
    def test_stream_chunk_processing(self):
        from scan_module.read_files import get_text_from_file_stream
        chunks = list(get_text_from_file_stream(self.large_file, chunk_size=1000))
        self.assertGreater(len(chunks), 1)
        combined = "".join(chunks)
        self.assertEqual(combined, self.content)
    
    def test_stream_custom_chunk_size(self):
        from scan_module.read_files import get_text_from_file_stream
        chunks = list(get_text_from_file_stream(self.large_file, chunk_size=500))
        self.assertEqual(len(chunks), 20)
    
    def test_stream_file_not_found(self):
        from scan_module.read_files import get_text_from_file_stream
        with self.assertRaises(FileNotFoundError):
            next(get_text_from_file_stream("nonexistent.txt"))

if __name__ == '__main__':
    unittest.main()