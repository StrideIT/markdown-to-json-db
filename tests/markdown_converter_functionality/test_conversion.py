"""
Unit tests for ConversionCoordinator.
"""

import unittest
import os
from markdown_converter.coordinators.conversion import ConversionCoordinator

class TestConversion(unittest.TestCase):
    """Test cases for ConversionCoordinator."""

    def setUp(self):
        """Set up test environment."""
        self.test_dir = os.path.join('tests', 'markdown_converter_functionality', 'test_files')
        os.makedirs(self.test_dir, exist_ok=True)
        
        # Create test files
        self.single_heading = os.path.join(self.test_dir, 'single_heading.md')
        with open(self.single_heading, 'w') as f:
            f.write("# Main Heading\nMain content")
            
        self.multiple_headings = os.path.join(self.test_dir, 'multiple_headings.md')
        with open(self.multiple_headings, 'w') as f:
            f.write("# First\nContent 1\n# Second\nContent 2")
            
        self.nested_headings = os.path.join(self.test_dir, 'nested_headings.md')
        with open(self.nested_headings, 'w') as f:
            f.write("# Main\n## Sub1\nContent 1\n## Sub2\nContent 2")
            
        self.empty_file = os.path.join(self.test_dir, 'empty.md')
        with open(self.empty_file, 'w') as f:
            f.write("")

    def tearDown(self):
        """Clean up test files."""
        test_files = [
            self.single_heading,
            self.multiple_headings,
            self.nested_headings,
            self.empty_file
        ]
        for file in test_files:
            if os.path.exists(file):
                os.remove(file)

    def test_single_heading(self):
        """Test converting file with single heading."""
        coordinator = ConversionCoordinator(self.single_heading)
        content = ["# Main Heading", "Main content"]
        result = coordinator.convert(content)
        
        self.assertIn('single_heading.md', result)
        doc = result['single_heading.md'][0]
        self.assertEqual(doc['title'], 'Main Heading')
        self.assertEqual(doc['content'], 'Main content')
        self.assertEqual(len(doc['children']), 0)

    def test_multiple_headings(self):
        """Test converting file with multiple headings."""
        coordinator = ConversionCoordinator(self.multiple_headings)
        content = ["# First", "Content 1", "# Second", "Content 2"]
        result = coordinator.convert(content)
        
        sections = result['multiple_headings.md']
        self.assertEqual(len(sections), 2)
        self.assertEqual(sections[0]['title'], 'First')
        self.assertEqual(sections[1]['title'], 'Second')

    def test_nested_headings(self):
        """Test converting file with nested headings."""
        coordinator = ConversionCoordinator(self.nested_headings)
        content = ["# Main", "## Sub1", "Content 1", "## Sub2", "Content 2"]
        result = coordinator.convert(content)
        
        doc = result['nested_headings.md'][0]
        self.assertEqual(doc['title'], 'Main')
        self.assertEqual(len(doc['children']), 2)
        self.assertEqual(doc['children'][0]['title'], 'Sub1')
        self.assertEqual(doc['children'][1]['title'], 'Sub2')

    def test_empty_content(self):
        """Test converting empty file."""
        coordinator = ConversionCoordinator(self.empty_file)
        content = []
        result = coordinator.convert(content)
        
        doc = result['empty.md'][0]
        self.assertEqual(doc['title'], 'Document')
        self.assertEqual(doc['content'], '')
        self.assertEqual(len(doc['children']), 0)

    def test_validation_valid(self):
        """Test validation of valid structure."""
        coordinator = ConversionCoordinator(self.single_heading)
        content = ["# Main Heading", "Main content"]
        data = coordinator.convert(content)
        
        is_valid, errors = coordinator.validate(data)
        self.assertTrue(is_valid)
        self.assertEqual(errors, '')

    def test_validation_invalid(self):
        """Test validation of invalid structure."""
        coordinator = ConversionCoordinator(self.single_heading)
        invalid_data = {'invalid': 'structure'}
        
        is_valid, errors = coordinator.validate(invalid_data)
        self.assertFalse(is_valid)
        self.assertNotEqual(errors, '')

if __name__ == '__main__':
    unittest.main()
