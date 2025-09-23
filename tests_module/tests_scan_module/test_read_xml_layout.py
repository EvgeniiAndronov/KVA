import os
import unittest
import sys
sys.path.append('../../scan_module')
from read_layout import _read_xml_layout

class TestReadXmlLayout(unittest.TestCase):
    
    def setUp(self):
        self.test_file = "test_xml.xml"
    
    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_standard_xml_format(self):
        xml_content = '''<?xml version="1.0"?>
        <layout>
            <key symbol="a" error="1"/>
            <key symbol="b" error="2"/>
            <key symbol="c" error="3"/>
        </layout>'''
        
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write(xml_content)
        
        result = _read_xml_layout(self.test_file)
        self.assertEqual(result, {"a": 1.0, "b": 2.0, "c": 3.0})
    
    def test_alternative_attributes(self):
        xml_content = '''<?xml version="1.0"?>
        <layout>
            <key char="a" value="1"/>
            <key letter="b" weight="2"/>
        </layout>'''
        
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write(xml_content)
        
        result = _read_xml_layout(self.test_file)
        self.assertEqual(result, {"a": 1.0, "b": 2.0})
    
    def test_empty_xml(self):
        xml_content = '''<?xml version="1.0"?>
        <layout>
        </layout>'''
        
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write(xml_content)
        
        result = _read_xml_layout(self.test_file)
        self.assertEqual(result, {})

if __name__ == '__main__':
    unittest.main()