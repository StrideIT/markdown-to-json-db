"""
Test runner for MarkdownConverter functionality tests.
"""

import unittest
import sys
import os
import time
from typing import Type, Optional

def run_test_with_retry(test_case: Type[unittest.TestCase], max_retries: int = 3) -> bool:
    """Run a test case with retry logic."""
    test_name = test_case.__name__
    
    for attempt in range(max_retries):
        print(f"\n=== Running {test_name} (Attempt {attempt + 1}/{max_retries}) ===")
        
        # Create and run test suite
        suite = unittest.TestLoader().loadTestsFromTestCase(test_case)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        if result.wasSuccessful():
            print(f"\n✅ {test_name} passed!")
            return True
            
        if attempt < max_retries - 1:
            print(f"\n❌ {test_name} failed, retrying...")
            time.sleep(1)  # Brief pause before retry
    
    print(f"\n❌ {test_name} failed after {max_retries} attempts, skipping...")
    return False

def run_all_tests() -> None:
    """Run all test suites with retry logic."""
    from test_file_operations import TestFileOperations
    from test_conversion import TestConversion
    from test_database import TestDatabase
    from test_integration import TestMarkdownConverterIntegration
    
    test_cases = [
        TestFileOperations,
        TestConversion,
        TestDatabase,
        TestMarkdownConverterIntegration
    ]
    
    results = {
        'passed': 0,
        'failed': 0,
        'total': len(test_cases)
    }
    
    print("\n=== Starting Test Execution ===")
    start_time = time.time()
    
    for test_case in test_cases:
        if run_test_with_retry(test_case):
            results['passed'] += 1
        else:
            results['failed'] += 1
    
    end_time = time.time()
    total_time = end_time - start_time
    
    # Print summary
    print("\n=== Test Execution Summary ===")
    print(f"Total Tests: {results['total']}")
    print(f"Passed: {results['passed']}")
    print(f"Failed: {results['failed']}")
    print(f"Total Time: {total_time:.2f} seconds")
    print("============================")
    
    # Exit with status code
    sys.exit(0 if results['failed'] == 0 else 1)

if __name__ == '__main__':
    # Add project root to Python path
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    
    run_all_tests()
