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
        self.source_file = source_file

    def read(self) -> List[str]:
        if not os.path.exists(self.source_file):
            raise FileNotFoundError(f"Source file not found: {self.source_file}")
        with open(self.source_file, 'r', encoding='utf-8') as f:
            return f.readlines()
