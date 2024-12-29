"""
Tests for the content accumulator component.
"""

import unittest
from markdown_converter.markdown_parser.content_accumulator import ContentAccumulator

class TestContentAccumulator(unittest.TestCase):
    """Test cases for ContentAccumulator class"""

    def setUp(self):
        self.accumulator = ContentAccumulator()

    def test_accumulate_single_block(self):
        """Test accumulation of a single content block"""
        content = [
            "# Heading",
            "This is content",
            "More content"
        ]
        result = self.accumulator.handle(content)
        
        self.assertIn('blocks', result)
        self.assertEqual(len(result['blocks']), 1)
        self.assertIn("This is content\nMore content", result['blocks'][0])

    def test_accumulate_multiple_blocks(self):
        """Test accumulation of multiple content blocks"""
        content = [
            "# First Heading",
            "Content 1",
            "More content 1",
            "## Second Heading",
            "Content 2",
            "### Third Heading",
            "Content 3"
        ]
        result = self.accumulator.handle(content)
        
        self.assertEqual(len(result['blocks']), 3)
        self.assertIn("Content 1\nMore content 1", result['blocks'][0])
        self.assertIn("Content 2", result['blocks'][1])
        self.assertIn("Content 3", result['blocks'][2])

    def test_handle_empty_content(self):
        """Test handling of empty content"""
        result = self.accumulator.handle([])
        self.assertEqual(result['blocks'], [])

    def test_handle_only_headings(self):
        """Test handling content with only headings"""
        content = [
            "# Heading 1",
            "## Heading 2",
            "### Heading 3"
        ]
        result = self.accumulator.handle(content)
        self.assertEqual(len(result['blocks']), 0)

    def test_handle_dict_content(self):
        """Test handling of dictionary content"""
        content = {
            'content': [
                "# Heading",
                "Some content"
            ]
        }
        result = self.accumulator.handle(content)
        
        self.assertIn('blocks', result)
        self.assertEqual(len(result['blocks']), 1)
        self.assertIn("Some content", result['blocks'][0])

    def test_preserve_empty_lines(self):
        """Test that empty lines between content are preserved"""
        content = [
            "# Heading",
            "First line",
            "",
            "Second line"
        ]
        result = self.accumulator.handle(content)
        
        self.assertEqual(len(result['blocks']), 1)
        self.assertIn("First line\n\nSecond line", result['blocks'][0])

if __name__ == '__main__':
    unittest.main()
