import os
from typing import List

"""
Author: Tariq Ahmed
Email: t.ahmed@stride.ae
Organization: Stride Information Technology

This module provides the FileReader class for reading the content of a file.
"""

class FileReader:
    def __init__(self, source_file: str):
        """
        Initialize the FileReader.

        Args:
            source_file (str): The path to the source file to be read.
        """
        self.source_file = source_file

    def read(self) -> List[str]:
        """
        Read the content of the source file.

        Returns:
            List[str]: A list of lines read from the source file.

        Raises:
            FileNotFoundError: If the source file does not exist.
        """
        if not os.path.exists(self.source_file):
            raise FileNotFoundError(f"Source file not found: {self.source_file}")
        with open(self.source_file, 'r', encoding='utf-8') as f:
            return f.readlines()
