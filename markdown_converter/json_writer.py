"""
JSON writer module for handling file output with proper formatting.

This module provides functionality to write JSON content to files while handling
directory creation, proper UTF-8 encoding, and consistent formatting. It ensures
that JSON output is both human-readable and properly structured.

Author:
    Tariq Ahmed (t.ahmed@stride.ae)

Organization:
    Stride Information Technology LLC

Attributes:
    output_path (str): Path where the JSON file will be written.

Example:
    >>> writer = JSONWriter("output/data.json")
    >>> writer.write({"key": "value"})
    >>> with open("output/data.json", "r") as f:
    ...     print("File created:", f.read().strip())
"""

import json
import os
from typing import Dict, Any

class JSONWriter:
    def __init__(self, output_path: str) -> None:
        """Initialize the JSONWriter with an output file path.

        This constructor sets up the JSONWriter instance with the path where
        the JSON file will be written. The actual directory creation is deferred
        until the write operation.

        Args:
            output_path (str): The path where the JSON file will be written.
                If the directory doesn't exist, it will be created during write.
                Should be a valid file path string with .json extension.

        Example:
            >>> writer = JSONWriter("output/data.json")
            >>> writer.output_path.endswith('.json')
            True
        """
        self.output_path = output_path

    def write(self, data: Dict[str, Any]) -> None:
        """Write the provided data as formatted JSON to the output file.

        This method handles the complete process of writing JSON data to a file:
        1. Creates the output directory structure if it doesn't exist
        2. Serializes the data to JSON with consistent formatting (2-space indent)
        3. Writes the content using UTF-8 encoding for universal compatibility

        Args:
            data (Dict[str, Any]): The data to be written as JSON.
                Must be JSON-serializable (containing only basic Python types:
                dict, list, str, int, float, bool, None).

        Raises:
            OSError: If directory creation fails or file cannot be written.
            TypeError: If data contains non-JSON-serializable types.
            ValueError: If data structure is invalid for JSON serialization.

        Example:
            >>> writer = JSONWriter("output/data.json")
            >>> data = {
            ...     "name": "example",
            ...     "values": [1, 2, 3],
            ...     "nested": {"key": "value"}
            ... }
            >>> writer.write(data)
            >>> import os
            >>> os.path.exists("output/data.json")
            True
        """
        if os.path.dirname(self.output_path):
            os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        with open(self.output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
