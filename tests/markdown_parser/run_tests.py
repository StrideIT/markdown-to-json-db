"""
Test runner for markdown parser components.
"""

import unittest
import sys
import os

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from test_base_handler import TestBaseHandler
from test_heading_detector import TestHeadingDetector
from test_content_accumulator import TestContentAccumulator
from test_tree_manager import TestTreeManager

def run_tests():
    """Run all test cases and return the result."""
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestBaseHandler))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestHeadingDetector))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestContentAccumulator))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestTreeManager))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return 0 if all tests passed, 1 otherwise
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_tests())
