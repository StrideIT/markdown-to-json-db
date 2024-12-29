"""
Unit tests for DatabaseOperationsCoordinator.
"""

import unittest
import os
from typing import Dict, Any, List, Tuple, Optional
from markdown_converter.coordinators.database_operations import DatabaseOperationsCoordinator

class TestDatabase(unittest.TestCase):
    """Test cases for DatabaseOperationsCoordinator."""

    def setUp(self):
        """Set up test environment."""
        self.coordinator = DatabaseOperationsCoordinator()
        self.test_dir = os.path.join('tests', 'markdown_converter_functionality', 'test_files')
        os.makedirs(self.test_dir, exist_ok=True)
        
        # Test data
        self.test_file = os.path.join(self.test_dir, 'test.md')
        self.test_data = {
            'test.md': [{
                'title': 'Main',
                'content': 'Content',
                'level': 1,
                'children': [{
                    'title': 'Sub',
                    'content': 'Sub content',
                    'level': 2,
                    'children': []
                }]
            }]
        }

    def tearDown(self):
        """Clean up test data."""
        self.coordinator.truncate_tables()

    def test_insert_document(self):
        """Test inserting a new document."""
        doc_id = self.coordinator.save(self.test_file, self.test_data)
        self.assertIsNotNone(doc_id)
        
        # Verify document exists
        doc = self.coordinator.get_document(doc_id)
        if doc is None:
            self.fail("Document not found")
        self.assertEqual(doc[1], self.test_file)

    def test_insert_duplicate_document(self):
        """Test inserting a duplicate document."""
        # Insert first time
        first_id = self.coordinator.save(self.test_file, self.test_data)
        self.assertIsNotNone(first_id)
        
        # Insert same document again
        second_id = self.coordinator.save(self.test_file, self.test_data)
        self.assertIsNotNone(second_id)
        
        # Should update existing document
        self.assertEqual(first_id, second_id)
        
        # Verify only one document exists
        doc = self.coordinator.get_document(first_id)
        if doc is None:
            self.fail("Document not found")
        self.assertEqual(doc[1], self.test_file)

    def test_insert_sections(self):
        """Test inserting document sections."""
        doc_id = self.coordinator.save(self.test_file, self.test_data)
        self.assertIsNotNone(doc_id)
        
        # Verify sections
        sections = self.coordinator.get_sections(doc_id)
        self.assertEqual(len(sections), 2)  # Main section and subsection
        
        # Find sections by title
        def find_section(title: str) -> Optional[Tuple[int, Optional[int], str, str, int]]:
            return next((s for s in sections if s[2] == title), None)
        
        # Verify hierarchy
        main_section = find_section('Main')
        sub_section = find_section('Sub')
        
        if main_section is None or sub_section is None:
            self.fail("Required sections not found")
            
        self.assertIsNone(main_section[1])  # Main section has no parent
        self.assertEqual(sub_section[1], main_section[0])  # Sub section's parent is main section

    def test_update_sections(self):
        """Test updating existing sections."""
        # Insert initial document
        doc_id = self.coordinator.save(self.test_file, self.test_data)
        self.assertIsNotNone(doc_id)
        
        # Update with modified data
        modified_data = self.test_data.copy()
        modified_data['test.md'][0]['content'] = 'Updated content'
        self.coordinator.save(self.test_file, modified_data)
        
        # Verify update
        sections = self.coordinator.get_sections(doc_id)
        main_section = next((s for s in sections if s[2] == 'Main'), None)
        if main_section is None:
            self.fail("Main section not found")
        self.assertEqual(main_section[3], 'Updated content')

    def test_validation_result(self):
        """Test storing validation results."""
        doc_id = self.coordinator.save(self.test_file, self.test_data)
        self.assertIsNotNone(doc_id)
        
        # Verify validation result
        result = self.coordinator.get_validation_result(doc_id)
        if result is None:
            self.fail("Validation result not found")
        self.assertTrue(result[1])  # is_valid should be True
        self.assertEqual(result[2], '')  # No errors

if __name__ == '__main__':
    unittest.main()
