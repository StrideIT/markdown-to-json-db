"""
Schema validator module for document structure validation.

This module provides validation for document schema compliance, ensuring
all required fields are present and have the correct types. It implements
the validation strategy pattern for schema integrity checks.

Author:
    Tariq Ahmed (t.ahmed@stride.ae)

Organization:
    Stride Information Technology LLC

Example:
    >>> validator = SchemaValidator()
    >>> data = {
    ...     "doc.md": [{
    ...         "title": "Section",
    ...         "content": "Content here",
    ...         "level": 1,
    ...         "children": []
    ...     }]
    ... }
    >>> is_valid, error = validator.validate(data)
    >>> print("Valid schema" if is_valid else f"Invalid: {error}")
"""

from typing import Dict, Any, Tuple, Optional, Set
from .base.base_validator import ValidationStrategy
from .base.error_handler import ValidationError

class SchemaValidator(ValidationStrategy):
    """Validates document schema structure and field types.

    This validator ensures that document data follows the expected schema,
    including:
    1. Required fields presence (title, content, level, children)
    2. Correct field types (str for title/content, int for level, etc.)
    3. Proper nesting of sections and their children

    The validator uses the ValidationStrategy pattern and provides detailed
    error messages through the ErrorFormatter for any schema violations.

    Attributes:
        error_formatter (ErrorFormatter): Utility for consistent error messages
        required_fields (Set[str]): Set of required section fields
    """

    def __init__(self):
        """Initialize schema validator with required fields."""
        super().__init__()
        self.required_fields: Set[str] = {'title', 'content', 'level', 'children'}

    def validate(self, data: Dict[str, Any]) -> Tuple[bool, Optional[ValidationError]]:
        """Validate document schema compliance.

        Performs comprehensive schema validation, ensuring all required
        fields are present and have correct types. This includes checking
        both top-level structure and recursive validation of sections.

        Args:
            data (Dict[str, Any]): Document data to validate, containing:
                - Filename as key
                - List of sections as value, where each section must have:
                    - title (str): Section heading
                    - content (str): Section content
                    - level (int): Section level (1-6)
                    - children (List): List of subsections

        Returns:
            Tuple[bool, Optional[ValidationError]]: A tuple containing:
                - bool: True if schema is valid, False otherwise
                - Optional[ValidationError]: Error details if invalid,
                  None if valid

        Example:
            >>> validator = SchemaValidator()
            >>> data = {
            ...     "doc.md": [{
            ...         "title": "Test",
            ...         "content": "",
            ...         "level": 1,
            ...         "children": []
            ...     }]
            ... }
            >>> valid, error = validator.validate(data)
            >>> if not valid:
            ...     print(f"Schema error: {error}")
        """
        try:
            # Validate top level structure
            if not self._check_type(data, dict, "Document data"):
                return False, ValidationError(
                    self.error_formatter.format_type_error(data, dict, "Document data")
                )
            if not self._check_not_empty(data, "Document data"):
                return False, ValidationError(
                    self.error_formatter.format_empty_error("Document data")
                )

            # Validate each document section
            for filename, sections in data.items():
                if not self._check_type(filename, str, "Filename"):
                    return False, ValidationError(
                        self.error_formatter.format_type_error(filename, str, "Filename")
                    )
                if not self._check_type(sections, list, f"Sections for {filename}"):
                    return False, ValidationError(
                        self.error_formatter.format_type_error(sections, list, f"Sections for {filename}")
                    )

                # Validate each section
                for section in sections:
                    valid, error = self._validate_section(section, filename)
                    if not valid:
                        return False, error

            return True, None
        except Exception as e:
            return False, ValidationError(str(e))

    def _validate_section(self, section: Dict[str, Any], context: str) -> Tuple[bool, Optional[ValidationError]]:
        """Validate an individual document section.

        Performs detailed validation of a single section, checking required
        fields, field types, and recursively validating child sections.

        Args:
            section (Dict[str, Any]): Section data to validate
            context (str): Document/section context for error messages

        Returns:
            Tuple[bool, Optional[ValidationError]]: A tuple containing:
                - bool: True if section is valid, False otherwise
                - Optional[ValidationError]: Error details if invalid,
                  None if valid

        Example:
            >>> validator = SchemaValidator()
            >>> section = {
            ...     "title": "Section",
            ...     "content": "Content",
            ...     "level": 1,
            ...     "children": []
            ... }
            >>> valid, error = validator._validate_section(
            ...     section, "doc.md"
            ... )
        """
        # Validate section is a dictionary
        if not self._check_type(section, dict, f"Section in {context}"):
            return False, ValidationError(
                self.error_formatter.format_type_error(section, dict, f"Section in {context}")
            )

        # Check required fields
        missing = self.required_fields - section.keys()
        if missing:
            return False, ValidationError(
                self.error_formatter.format_missing_field_error(
                    ', '.join(missing),
                    f"Section in {context}"
                )
            )

        # Validate field types
        field_types = {
            'title': (str, "Title"),
            'content': (str, "Content"),
            'level': (int, "Level"),
            'children': (list, "Children")
        }

        for field, (expected_type, field_name) in field_types.items():
            if not self._check_type(section[field], expected_type, f"{field_name} in {context}"):
                return False, ValidationError(
                    self.error_formatter.format_type_error(
                        section[field],
                        expected_type,
                        f"{field_name} in {context}"
                    )
                )

        # Recursively validate children
        for child in section['children']:
            valid, error = self._validate_section(child, f"{context} -> {section['title']}")
            if not valid:
                return False, error

        return True, None
