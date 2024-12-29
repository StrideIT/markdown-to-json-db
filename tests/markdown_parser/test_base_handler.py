"""
Tests for the base parser handler.
"""

import unittest
from markdown_converter.markdown_parser.base_handler import ParserHandler
from typing import Dict, Any

class TestHandler(ParserHandler):
    """Test implementation of ParserHandler"""
    def handle(self, content: Any) -> Dict[str, Any]:
        return {"test": True}

class TestBaseHandler(unittest.TestCase):
    """Test cases for ParserHandler base class"""

    def setUp(self):
        self.handler = TestHandler()

    def test_handler_interface(self):
        """Test that handler interface works correctly"""
        result = self.handler.handle("test content")
        self.assertIsInstance(result, dict)
        self.assertTrue(result.get("test"))

    def test_handler_with_empty_content(self):
        """Test handler with empty content"""
        result = self.handler.handle("")
        self.assertIsInstance(result, dict)

    def test_handler_with_none_content(self):
        """Test handler with None content"""
        result = self.handler.handle(None)
        self.assertIsInstance(result, dict)

if __name__ == '__main__':
    unittest.main()
