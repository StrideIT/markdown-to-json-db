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
        self.output_path = output_path

    def write(self, data: dict):
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        with open(self.output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
