import unittest

class TestExtractLayoutFromDict(unittest.TestCase):
    
    def test_direct_layout(self):
        from scan_module.read_layout import _extract_layout_from_dict
        data = {"a": 1, "b": 2, "c": 3}
        result = _extract_layout_from_dict(data)
        self.assertEqual(result, data)
    
    def test_nested_layout_key(self):
        from scan_module.read_layout import _extract_layout_from_dict
        data = {"layout": {"a": 1, "b": 2}}
        result = _extract_layout_from_dict(data)
        self.assertEqual(result, {"a": 1, "b": 2})
    
    def test_alternative_nested_keys(self):
        from scan_module.read_layout import _extract_layout_from_dict
        for key in ["keyboard_layout", "rules", "mapping", "keys"]:
            data = {key: {"a": 1, "b": 2}}
            result = _extract_layout_from_dict(data)
            self.assertEqual(result, {"a": 1, "b": 2})
    
    def test_invalid_data(self):
        from scan_module.read_layout import _extract_layout_from_dict
        with self.assertRaises(ValueError):
            _extract_layout_from_dict("invalid data")

if __name__ == '__main__':
    unittest.main()