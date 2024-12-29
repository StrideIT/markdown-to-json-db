"""
Core module for converting Markdown files to JSON with database integration.

This module serves as the main entry point for the markdown-to-json conversion
system. It orchestrates the entire conversion process through specialized
coordinators that handle different aspects: file operations for I/O, content
conversion for parsing, and database operations for persistent storage.

Author:
    Tariq Ahmed (t.ahmed@stride.ae)

Organization:
    Stride Information Technology LLC

Example:
    >>> # Basic conversion to JSON file
    >>> converter = MarkdownConverter("input.md")
    >>> output_path = converter.convert()
    >>> print(f"JSON saved to: {output_path}")
    
    >>> # Conversion with database storage
    >>> converter_with_db = MarkdownConverter("input.md", save_to_db=True)
    >>> output_path = converter_with_db.convert()
    >>> print(f"JSON saved to file and database")
"""

from typing import Optional
from .coordinators import (
    FileOperationsCoordinator,
    ConversionCoordinator,
    DatabaseOperationsCoordinator
)

class MarkdownConverter:
    """Main converter class orchestrating the markdown to JSON transformation.

    This class coordinates three main aspects of the conversion process:
    1. File Operations: Reading markdown and writing JSON
    2. Content Conversion: Parsing markdown into structured data
    3. Database Operations: Optional persistent storage of converted content

    The conversion process is designed to be flexible, allowing output to
    both file system and database, with database storage being optional.

    Attributes:
        file_coordinator (FileOperationsCoordinator): Handles file I/O operations
        conversion_coordinator (ConversionCoordinator): Manages content parsing
        db_coordinator (Optional[DatabaseOperationsCoordinator]): Handles database
            operations when enabled
    """

    def __init__(self, source_file: str, output_path: Optional[str] = None, save_to_db: bool = False) -> None:
        """Initialize the MarkdownConverter with source file and options.

        Sets up the conversion pipeline by initializing the necessary coordinators
        based on the provided options. The file and conversion coordinators are
        always created, while the database coordinator is optional.

        Args:
            source_file (str): Path to the source Markdown file to convert.
                Should be a valid path to an existing markdown file.
            output_path (Optional[str], optional): Path where the JSON output
                will be written. If None, uses the same path as source_file
                with .json extension. Defaults to None.
            save_to_db (bool, optional): Whether to save the output to the
                database. When True, initializes database operations.
                Defaults to False.

        Example:
            >>> # Basic conversion setup
            >>> converter = MarkdownConverter("doc.md")
            >>> isinstance(converter.file_coordinator, FileOperationsCoordinator)
            True
            
            >>> # Setup with custom output and database storage
            >>> converter = MarkdownConverter(
            ...     "doc.md",
            ...     output_path="custom/path.json",
            ...     save_to_db=True
            ... )
            >>> converter.db_coordinator is not None
            True
        """
        self.file_coordinator = FileOperationsCoordinator(source_file, output_path)
        self.conversion_coordinator = ConversionCoordinator(source_file)
        self.db_coordinator = DatabaseOperationsCoordinator() if save_to_db else None

    def convert(self) -> str:
        """Execute the markdown to JSON conversion process.

        Performs the complete conversion process in the following steps:
        1. Reads the markdown content from the source file
        2. Converts the content to a structured JSON format
        3. Writes the JSON output to the specified file
        4. Optionally saves the data to the database if enabled
        
        Returns:
            str: The path to the converted JSON file. This is either the
                custom output_path if provided during initialization, or
                the default path derived from the source file.

        Raises:
            FileNotFoundError: If the source file cannot be read
            OSError: If the output file cannot be written
            ValueError: If the markdown content is invalid
            RuntimeError: If database operations fail when enabled

        Example:
            >>> converter = MarkdownConverter("doc.md")
            >>> output_path = converter.convert()
            >>> output_path.endswith(".json")
            True
            >>> import os
            >>> os.path.exists(output_path)
            True
        """
        content = self.file_coordinator.read_content()
        data = self.conversion_coordinator.convert(content)
        self.file_coordinator.write_json(data)
        
        if self.db_coordinator:
            self.db_coordinator.save(self.file_coordinator.source_file, data)
        
        return self.file_coordinator.get_output_path()
