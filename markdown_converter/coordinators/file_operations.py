"""
File operations coordinator module for I/O management.

This module provides a centralized coordinator for all file-related operations
in the markdown conversion process. It manages file reading, writing, and path
handling while ensuring proper error handling and UTF-8 encoding support.

Author:
    Tariq Ahmed (t.ahmed@stride.ae)

Organization:
    Stride Information Technology LLC

Example:
    >>> coordinator = FileOperationsCoordinator("input.md")
    >>> content = coordinator.read_content()
    >>> coordinator.write_json({"input.md": [{"title": "Test"}]})
    >>> print(coordinator.get_output_path().endswith(".json"))
    True
"""

from typing import Optional, Dict, Any, List
from ..file_reader import FileReader
from ..json_writer import JSONWriter
from ..path_manager import PathManager

class FileOperationsCoordinator:
    """Coordinates file system operations for markdown conversion.

    This class manages all file-related operations including:
    1. Path normalization and validation
    2. Directory creation and management
    3. File reading with UTF-8 support
    4. JSON writing with proper formatting

    The coordinator uses specialized handlers for each type of operation
    while providing a unified interface for file operations.

    Attributes:
        path_manager (PathManager): Handles path operations and validation
        source_file (str): Normalized path to source markdown file
        output_path (str): Normalized path for JSON output
        file_reader (FileReader): Handles file reading operations
        json_writer (JSONWriter): Handles JSON writing operations
    """

    def __init__(self, source_file: str, output_path: Optional[str] = None) -> None:
        """Initialize the file operations coordinator.

        Sets up the coordinator with source and output paths, creating
        necessary directories and validating paths. If no output path is
        provided, generates a default one based on the source file.

        Args:
            source_file (str): Path to the source markdown file.
            output_path (Optional[str], optional): Path where JSON output
                will be written. If None, uses default path derived from
                source file. Defaults to None.

        Raises:
            FileNotFoundError: If source file doesn't exist or is inaccessible
            OSError: If output directory cannot be created

        Example:
            >>> coordinator = FileOperationsCoordinator(
            ...     "doc.md",
            ...     output_path="output/doc.json"
            ... )
            >>> print(coordinator.output_path.endswith(".json"))
            True
        """
        self.path_manager = PathManager()
        self.source_file = self.path_manager.normalize_path(source_file)
        self.output_path = (self.path_manager.normalize_path(output_path) 
                          if output_path 
                          else self.path_manager.get_default_output_path(self.source_file))
        
        if not self.path_manager.validate_path(self.source_file):
            raise FileNotFoundError(f"Source file not found: {self.source_file}")
            
        self.path_manager.ensure_directory(self.output_path)
        self.file_reader = FileReader(self.source_file)
        self.json_writer = JSONWriter(self.output_path)

    def read_content(self) -> List[str]:
        """Read content from the source markdown file.

        Reads the entire source file using UTF-8 encoding, returning
        the content as a list of lines. Each line maintains its
        original formatting.

        Returns:
            List[str]: List of lines from the source file.

        Raises:
            FileNotFoundError: If source file cannot be read
            UnicodeDecodeError: If file content is not valid UTF-8

        Example:
            >>> coordinator = FileOperationsCoordinator("doc.md")
            >>> content = coordinator.read_content()
            >>> print(f"Read {len(content)} lines")
        """
        return self.file_reader.read()

    def write_json(self, data: Dict[str, Any]) -> None:
        """Write converted data as formatted JSON.

        Writes the provided data structure to the output file in JSON
        format with proper indentation and UTF-8 encoding. Creates
        parent directories if they don't exist.

        Args:
            data (Dict[str, Any]): The data structure to write as JSON.
                Should be a valid, serializable dictionary.

        Raises:
            OSError: If file cannot be written or directory created
            TypeError: If data is not JSON-serializable

        Example:
            >>> coordinator = FileOperationsCoordinator("doc.md")
            >>> data = {"doc.md": [{"title": "Section"}]}
            >>> coordinator.write_json(data)
            >>> import os
            >>> print(os.path.exists(coordinator.output_path))
            True
        """
        self.json_writer.write(data)

    def get_output_path(self) -> str:
        """Get the configured JSON output file path.

        Returns the full, normalized path where the JSON output will
        be or has been written.

        Returns:
            str: Absolute path to the JSON output file.

        Example:
            >>> coordinator = FileOperationsCoordinator("doc.md")
            >>> path = coordinator.get_output_path()
            >>> print(path.endswith(".json"))
            True
        """
        return self.output_path
