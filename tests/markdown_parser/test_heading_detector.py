"""
Tests for the heading detector component.
"""

import unittest
from markdown_converter.markdown_parser.heading_detector import HeadingDetector

class TestHeadingDetector(unittest.TestCase):
    """Test cases for HeadingDetector class"""

    def setUp(self):
        self.detector = HeadingDetector()

    def test_detect_single_heading(self):
        """Test detection of a single heading"""
        content = ["# Test Heading"]
        result = self.detector.handle(content)
        
        self.assertIn('headings', result)
        self.assertEqual(len(result['headings']), 1)
        self.assertEqual(result['headings'][0]['level'], 1)
        self.assertEqual(result['headings'][0]['title'], "Test Heading")

    def test_detect_multiple_headings(self):
        """Test detection of multiple headings"""
        content = [
            "# Heading 1",
            "## Heading 2",
            "### Heading 3"
        ]
        result = self.detector.handle(content)
        
        self.assertEqual(len(result['headings']), 3)
        self.assertEqual(result['headings'][0]['level'], 1)
        self.assertEqual(result['headings'][1]['level'], 2)
        self.assertEqual(result['headings'][2]['level'], 3)

    def test_ignore_invalid_headings(self):
        """Test that invalid headings are ignored"""
        content = [
            "#Invalid Heading",  # No space after #
            "Not a heading",
            "###### Valid Heading"  # Valid h6 heading
        ]
        result = self.detector.handle(content)
        
        self.assertEqual(len(result['headings']), 1)
        self.assertEqual(result['headings'][0]['level'], 6)
        self.assertEqual(result['headings'][0]['title'], "Valid Heading")

    def test_handle_empty_content(self):
        """Test handling of empty content"""
        result = self.detector.handle([])
        self.assertEqual(result['headings'], [])

    def test_handle_dict_content(self):
        """Test handling of dictionary content"""
        content = {
            'content': ["# Test Heading"]
        }
        result = self.detector.handle(content)
        
        self.assertIn('headings', result)
        self.assertEqual(len(result['headings']), 1)

if __name__ == '__main__':
    unittest.main()
