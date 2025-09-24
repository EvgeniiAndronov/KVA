import os
import unittest
from unittest.mock import patch

class TestGetFileSizeMb(unittest.TestCase):
    
    def setUp(self):
        self.test_file = "test_file.txt"
        with open(self.test_file, "w") as f:
            f.write("test content")
    
    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_get_file_size_existing_file(self):
        from scan_module.read_files import get_file_size_mb
        size = get_file_size_mb(self.test_file)
        self.assertGreaterEqual(size, 0)
        self.assertIsInstance(size, float)
    
    def test_get_file_size_nonexistent_file(self):
        from scan_module.read_files import get_file_size_mb
        size = get_file_size_mb("nonexistent_file.txt")
        self.assertEqual(size, 0)
    
    def test_get_file_size_large_file(self):
        from scan_module.read_files import get_file_size_mb
        with open("large_test_file.txt", "wb") as f:
            f.write(b"0" * 1024 * 1024)  # 1MB file
        
        size = get_file_size_mb("large_test_file.txt")
        self.assertAlmostEqual(size, 1.0, places=1)
        os.remove("large_test_file.txt")

if __name__ == '__main__':
    unittest.main()