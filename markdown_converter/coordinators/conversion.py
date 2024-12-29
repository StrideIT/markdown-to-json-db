"""
Conversion coordinator module for markdown to JSON transformation.

This module orchestrates the complete conversion process from markdown content
to validated JSON format. It coordinates the parsing and validation steps,
ensuring the output meets all structural and content requirements.

Author:
    Tariq Ahmed (t.ahmed@stride.ae)

Organization:
    Stride Information Technology LLC

Example:
    >>> coordinator = ConversionCoordinator("example.md")
    >>> content = ["# Title", "", "Content here"]
    >>> result = coordinator.convert(content)
    >>> print("Title" in result["example.md"][0]["title"])
    True
"""

from typing import Dict, Any, List, Tuple
from ..parser import MarkdownParser
from ..validator import Validator

class ConversionCoordinator:
    """Coordinates the markdown to JSON conversion process.

    This class manages the complete conversion pipeline, orchestrating the
    interaction between the parser and validator components. It ensures
    that markdown content is properly parsed into a structured format and
    validates the result against defined rules.

    The conversion process follows these steps:
    1. Parse markdown content into structured data
    2. Validate the structure and content
    3. Return the validated JSON format

    Attributes:
        parser (MarkdownParser): Handles markdown parsing
        validator (Validator): Ensures data validity
    """

    def __init__(self, source_file: str):
        """Initialize the ConversionCoordinator."""
        self.parser = MarkdownParser(source_file)
        self.validator = Validator()

    def convert(self, content: List[str]) -> Dict[str, Any]:
        """Convert markdown content to validated JSON format.

        Takes a list of markdown content lines and processes them through
        the conversion pipeline, producing a structured and validated
        JSON format.

        Args:
            content (List[str]): Lines of markdown content to convert.
                Each string in the list represents one line from the
                source file.

        Returns:
            Dict[str, Any]: Converted and validated JSON structure where:
                - Top level key is the source filename
                - Value is a list of section dictionaries
                - Each section has title, content, level, and children

        Raises:
            ValidationError: If the converted data fails validation

        Example:
            >>> coordinator = ConversionCoordinator("doc.md")
            >>> content = ["# Section", "", "Content"]
            >>> result = coordinator.convert(content)
            >>> print(result["doc.md"][0]["title"])
            'Section'
        """
        data = self.parser.parse(content)
        self.validator.validate(data)
        return data

    def validate(self, data: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate converted data against defined rules.

        Performs comprehensive validation of the converted data structure,
        checking for proper schema, content requirements, and structural
        integrity.

        Args:
            data (Dict[str, Any]): The converted data structure to
                validate. Should follow the expected schema with
                proper section hierarchy.

        Returns:
            Tuple[bool, str]: A tuple containing:
                - bool: True if validation passes, False otherwise
                - str: Error message if validation fails, empty if passes

        Example:
            >>> coordinator = ConversionCoordinator("doc.md")
            >>> data = {"doc.md": [{"title": "Test", "level": 1}]}
            >>> valid, error = coordinator.validate(data)
            >>> if not valid:
            ...     print(f"Validation failed: {error}")
        """
        return self.validator.validate(data)
