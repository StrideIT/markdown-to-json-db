import json
import os

"""
Author: Tariq Ahmed
Email: t.ahmed@stride.ae
Organization: Stride Information Technology

This module provides the JSONWriter class for writing JSON content to a file.
"""

class JSONWriter:
    def __init__(self, output_path: str):
        """
        Initialize the JSONWriter.

        Args:
            output_path (str): The path to save the JSON output file.
        """
        self.output_path = output_path

    def write(self, data: dict):
        """
        Write the JSON content to the output file.

        Args:
            data (dict): The JSON data to be written to the file.
        """
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        with open(self.output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
