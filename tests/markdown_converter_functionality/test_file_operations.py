"""
Unit tests for FileOperationsCoordinator.
"""

import unittest
import os
import json
from markdown_converter.coordinators.file_operations import FileOperationsCoordinator

class TestFileOperations(unittest.TestCase):
    """Test cases for FileOperationsCoordinator."""

    def setUp(self):
        """Set up test environment."""
        self.test_dir = os.path.join('tests', 'markdown_converter_functionality', 'test_files')
        os.makedirs(self.test_dir, exist_ok=True)
        
        # Create test markdown file
        self.test_md = os.path.join(self.test_dir, 'test.md')
        with open(self.test_md, 'w') as f:
            f.write("# Test\nContent")
            
        # Create empty file
        self.empty_md = os.path.join(self.test_dir, 'empty.md')
        with open(self.empty_md, 'w') as f:
            f.write("")

    def tearDown(self):
        """Clean up test files."""
        test_files = [
            self.test_md,
            self.empty_md,
            self.test_md.replace('.md', '.json'),
            self.empty_md.replace('.md', '.json')
        ]
        for file in test_files:
            if os.path.exists(file):
                os.remove(file)

    def test_read_valid_file(self):
        """Test reading a valid markdown file."""
        coordinator = FileOperationsCoordinator(self.test_md)
        content = coordinator.read_content()
        self.assertEqual(len(content), 2)
        self.assertEqual(content[0], "# Test")
        self.assertEqual(content[1], "Content")

    def test_read_empty_file(self):
        """Test reading an empty file."""
        coordinator = FileOperationsCoordinator(self.empty_md)
        content = coordinator.read_content()
        self.assertEqual(len(content), 0)

    def test_read_nonexistent_file(self):
        """Test reading a nonexistent file."""
        with self.assertRaises(FileNotFoundError):
            FileOperationsCoordinator('nonexistent.md')

    def test_write_new_json(self):
        """Test writing JSON to a new file."""
        coordinator = FileOperationsCoordinator(self.test_md)
        test_data = {"test": "data"}
        coordinator.write_json(test_data)
        
        output_path = coordinator.get_output_path()
        self.assertTrue(os.path.exists(output_path))
        
        with open(output_path) as f:
            saved_data = json.load(f)
        self.assertEqual(saved_data, test_data)

    def test_write_existing_json(self):
        """Test writing JSON to an existing file."""
        coordinator = FileOperationsCoordinator(self.test_md)
        
        # Write initial data
        initial_data = {"initial": "data"}
        coordinator.write_json(initial_data)
        
        # Write new data
        new_data = {"new": "data"}
        coordinator.write_json(new_data)
        
        output_path = coordinator.get_output_path()
        with open(output_path) as f:
            saved_data = json.load(f)
        self.assertEqual(saved_data, new_data)

    def test_write_invalid_path(self):
        """Test writing to an invalid path."""
        invalid_path = os.path.join('nonexistent', 'dir', 'test.md')
        with self.assertRaises(FileNotFoundError):
            FileOperationsCoordinator(invalid_path)

if __name__ == '__main__':
    unittest.main()
