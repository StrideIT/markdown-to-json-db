"""
Integration tests for MarkdownConverter system.
"""

import unittest
import os
import json
from markdown_converter.markdown_converter import MarkdownConverter

class TestMarkdownConverterIntegration(unittest.TestCase):
    """Integration test cases for MarkdownConverter."""

    def setUp(self):
        """Set up test environment."""
        self.test_dir = os.path.join('tests', 'markdown_converter_functionality', 'test_files')
        os.makedirs(self.test_dir, exist_ok=True)
        
        # Create test markdown file with complex structure
        self.test_md = os.path.join(self.test_dir, 'complex.md')
        with open(self.test_md, 'w') as f:
            f.write("""# Main Heading
Main content here.

## Section 1
Section 1 content.

### Subsection 1.1
Deeper content.

## Section 2
Section 2 content.

### Subsection 2.1
More content here.

#### Deep Section
Very deep content.""")

    def tearDown(self):
        """Clean up test files."""
        test_files = [
            self.test_md,
            self.test_md.replace('.md', '.json')
        ]
        for file in test_files:
            if os.path.exists(file):
                os.remove(file)

    def test_complete_conversion_flow(self):
        """Test complete conversion flow."""
        # Convert markdown to JSON
        converter = MarkdownConverter(self.test_md)
        output_path = converter.convert()
        
        # Verify output file exists
        self.assertTrue(os.path.exists(output_path))
        
        # Verify JSON structure
        with open(output_path) as f:
            data = json.load(f)
        
        # Check document structure
        self.assertIn('complex.md', data)
        root = data['complex.md'][0]
        
        # Check main heading
        self.assertEqual(root['title'], 'Main Heading')
        self.assertIn('Main content', root['content'])
        
        # Check sections
        self.assertEqual(len(root['children']), 2)  # Two main sections
        
        # Check Section 1
        section1 = root['children'][0]
        self.assertEqual(section1['title'], 'Section 1')
        self.assertEqual(len(section1['children']), 1)  # One subsection
        
        # Check Subsection 1.1
        subsection1 = section1['children'][0]
        self.assertEqual(subsection1['title'], 'Subsection 1.1')
        
        # Check Section 2
        section2 = root['children'][1]
        self.assertEqual(section2['title'], 'Section 2')
        self.assertEqual(len(section2['children']), 1)
        
        # Check deep nesting
        subsection2 = section2['children'][0]
        self.assertEqual(subsection2['title'], 'Subsection 2.1')
        self.assertEqual(len(subsection2['children']), 1)
        
        deep_section = subsection2['children'][0]
        self.assertEqual(deep_section['title'], 'Deep Section')

    def test_database_storage_flow(self):
        """Test conversion with database storage."""
        # Convert and store in database
        converter = MarkdownConverter(self.test_md, save_to_db=True)
        output_path = converter.convert()
        
        # Verify both file and database output
        self.assertTrue(os.path.exists(output_path))
        
        # Read converted data
        with open(output_path) as f:
            data = json.load(f)
        
        # Verify structure is preserved
        root = data['complex.md'][0]
        self.assertEqual(root['title'], 'Main Heading')
        self.assertTrue(len(root['children']) > 0)

    def test_error_handling_flow(self):
        """Test error handling in conversion flow."""
        # Create invalid markdown file
        invalid_md = os.path.join(self.test_dir, 'invalid.md')
        with open(invalid_md, 'w') as f:
            f.write("Invalid # Heading\nMalformed #content")
        
        try:
            # Should handle invalid content gracefully
            converter = MarkdownConverter(invalid_md)
            output_path = converter.convert()
            
            # Should still produce output
            self.assertTrue(os.path.exists(output_path))
            
            # Output should have a valid structure despite invalid input
            with open(output_path) as f:
                data = json.load(f)
            self.assertIn('invalid.md', data)
            
        finally:
            if os.path.exists(invalid_md):
                os.remove(invalid_md)
            json_path = invalid_md.replace('.md', '.json')
            if os.path.exists(json_path):
                os.remove(json_path)

if __name__ == '__main__':
    unittest.main()
