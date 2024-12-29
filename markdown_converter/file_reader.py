"""
File reader module for handling file content with UTF-8 encoding support.

This module provides functionality to read content from files while handling
common file operations and encoding issues. It ensures proper file handling
and consistent UTF-8 encoding across different platforms.

Author:
    Tariq Ahmed (t.ahmed@stride.ae)

Organization:
    Stride Information Technology LLC

Attributes:
    source_file (str): Path to the source file to be read.

Example:
    >>> reader = FileReader("path/to/file.md")
    >>> content = reader.read()
    >>> print(len(content), "lines read")
"""

import os
from typing import List

class FileReader:
    def __init__(self, source_file: str) -> None:
        """Initialize the FileReader with a source file path.

        This constructor sets up the FileReader instance with the path to the
        file that will be read. It performs basic validation of the input
        parameter but does not check file existence (that's done in read()).

        Args:
            source_file (str): The path to the source file to be read.
                This should be a valid file path string.

        Example:
            >>> reader = FileReader("path/to/file.md")
            >>> isinstance(reader.source_file, str)
            True
        """
        self.source_file = source_file

    def read(self) -> List[str]:
        """Read and return the content of the source file.

        This method opens the source file in UTF-8 encoding, reads all lines,
        and returns them as a list of strings. Each string in the list
        represents one line from the file, including the newline character
        if it was present.

        Returns:
            List[str]: A list of lines read from the source file. Each element
                is a string representing one line from the file.

        Raises:
            FileNotFoundError: If the source file does not exist or cannot be accessed.
            UnicodeDecodeError: If the file content cannot be decoded as UTF-8.

        Example:
            >>> reader = FileReader("path/to/file.md")
            >>> content = reader.read()
            >>> for line in content:
            ...     print(f"Line length: {len(line)}")
        """
        if not os.path.exists(self.source_file):
            raise FileNotFoundError(f"Source file not found: {self.source_file}")
        with open(self.source_file, 'r', encoding='utf-8') as f:
            return f.readlines()
