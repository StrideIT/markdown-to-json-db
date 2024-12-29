"""
Tests for the tree manager component.
"""

import unittest
from typing import Dict, Any
from markdown_converter.markdown_parser.tree_manager import TreeManager

class TestTreeManager(unittest.TestCase):
    """Test cases for TreeManager class"""

    def setUp(self):
        self.manager = TreeManager()

    def test_build_simple_tree(self):
        """Test building a simple tree structure"""
        content: Dict[str, Any] = {
            'headings': [
                {'level': 1, 'title': 'H1', 'content': ''},
                {'level': 2, 'title': 'H2', 'content': ''}
            ],
            'blocks': ['Content 1', 'Content 2']
        }
        result = self.manager.handle(content)
        
        self.assertIn('tree', result)
        tree = result['tree']
        self.assertEqual(len(tree), 1)
        self.assertEqual(tree[0]['title'], 'H1')
        self.assertEqual(len(tree[0]['children']), 1)
        self.assertEqual(tree[0]['children'][0]['title'], 'H2')

    def test_build_complex_tree(self):
        """Test building a complex tree structure"""
        content: Dict[str, Any] = {
            'headings': [
                {'level': 1, 'title': 'H1', 'content': ''},
                {'level': 2, 'title': 'H2-1', 'content': ''},
                {'level': 3, 'title': 'H3', 'content': ''},
                {'level': 2, 'title': 'H2-2', 'content': ''}
            ],
            'blocks': ['Content 1', 'Content 2', 'Content 3', 'Content 4']
        }
        result = self.manager.handle(content)
        
        tree = result['tree']
        self.assertEqual(len(tree), 1)
        h1 = tree[0]
        self.assertEqual(h1['title'], 'H1')
        self.assertEqual(len(h1['children']), 2)
        self.assertEqual(h1['children'][0]['title'], 'H2-1')
        self.assertEqual(len(h1['children'][0]['children']), 1)
        self.assertEqual(h1['children'][1]['title'], 'H2-2')

    def test_handle_empty_content(self):
        """Test handling of empty content"""
        result = self.manager.handle({})
        self.assertEqual(result['tree'], [])

    def test_handle_invalid_content(self):
        """Test handling of invalid content type"""
        result = self.manager.handle({'invalid': 'content'})
        self.assertEqual(result['tree'], [])

    def test_handle_missing_blocks(self):
        """Test handling content with missing blocks"""
        content: Dict[str, Any] = {
            'headings': [
                {'level': 1, 'title': 'H1', 'content': ''},
                {'level': 2, 'title': 'H2', 'content': ''}
            ]
        }
        result = self.manager.handle(content)
        
        tree = result['tree']
        self.assertEqual(len(tree), 1)
        self.assertEqual(tree[0]['content'], '')

    def test_handle_level_skipping(self):
        """Test handling of skipped heading levels"""
        content: Dict[str, Any] = {
            'headings': [
                {'level': 1, 'title': 'H1', 'content': ''},
                {'level': 3, 'title': 'H3', 'content': ''}  # Skips level 2
            ],
            'blocks': ['Content 1', 'Content 2']
        }
        result = self.manager.handle(content)
        
        tree = result['tree']
        self.assertEqual(len(tree), 1)
        h1 = tree[0]
        self.assertEqual(h1['title'], 'H1')
        self.assertEqual(len(h1['children']), 1)
        self.assertEqual(h1['children'][0]['title'], 'H3')

if __name__ == '__main__':
    unittest.main()
