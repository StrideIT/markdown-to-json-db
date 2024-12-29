"""
Test runner script for the markdown conversion system.

This script serves as the entry point for running all unit tests in the
project. It uses Python's unittest framework to discover and execute tests
in the 'tests' directory and its subdirectories.

Author:
    Tariq Ahmed (t.ahmed@stride.ae)

Organization:
    Stride Information Technology LLC

Usage:
    Run all tests:
        $ python run_tests.py

    This will:
    1. Discover all test files in the 'tests' directory
    2. Execute all test cases
    3. Report test results including passes, failures, and errors
"""

import unittest

def main() -> None:
    """Execute all project test cases.

    Uses unittest's test discovery to find and run all tests in the
    'tests' directory. The discovery process looks for files matching
    the pattern 'test_*.py' and executes all test cases within them.

    The tests are organized into several categories:
    - Markdown parser tests
    - Conversion functionality tests
    - Database integration tests
    - File operation tests

    Example:
        >>> main()
        # Test output will show here...
        ----------------------------------------------------------------------
        Ran X tests in Ys
        OK
    """
    unittest.main(module=None, argv=["unittest", "discover", "-s", "tests"])

if __name__ == "__main__":
    main()
