"""
Main script for markdown to JSON conversion with database integration.

This script serves as the entry point for the markdown conversion system,
demonstrating both file-based and database-integrated conversion scenarios.
It provides a command-line interface for converting markdown files to JSON
while optionally storing the results in a PostgreSQL database.

Author:
    Tariq Ahmed (t.ahmed@stride.ae)

Organization:
    Stride Information Technology LLC

Features:
    - Environment variable configuration via .env
    - Multiple conversion scenarios:
        1. File + Database storage
        2. File-only storage
    - Database table management utilities
    - Conversion status reporting

Example:
    To run the converter:
        $ python convert_md_to_json.py

    This will process the example file and demonstrate both:
    - Combined file and database storage
    - File-only storage
"""

import os
from dotenv import load_dotenv
from markdown_converter.markdown_converter import MarkdownConverter

# Load environment variables from .env file
load_dotenv()

import os

def truncate_tables() -> None:
    """Reset all database tables to a clean state.

    Executes the database truncation script to clear all tables while
    maintaining the schema. This is useful for testing or resetting
    the system to a known state.

    Note:
        This function requires the virtual environment to be properly
        configured and the database to be accessible.
    """

def main() -> None:
    """Execute the main conversion scenarios.

    Demonstrates two conversion scenarios:
    1. Full conversion with both file and database storage
    2. File-only conversion without database integration

    Both scenarios use the same input file but demonstrate different
    storage strategies. The function reports the output locations
    for verification.

    Note:
        The database scenario requires proper database configuration
        through environment variables.

    Example:
        >>> main()
        Output saved to: example/output/convert_test.json and database
        Output saved to: example/output/convert_test.json
    """
    # Scenario 1: Saving in both local folder and database
    converter_with_db = MarkdownConverter("example/convert_test.md", save_to_db=True)
    output_path_with_db = converter_with_db.convert()
    print(f"Output saved to: {output_path_with_db} and database")

    # Scenario 2: File-only storage
    converter_without_db = MarkdownConverter("example/convert_test.md", save_to_db=False)
    output_path_without_db = converter_without_db.convert()
    print(f"Output saved to: {output_path_without_db}")

if __name__ == "__main__":
    main()
