"""
Content validator module for document content validation.

This module provides validation for document content values, ensuring
that titles are not empty and content fields contain valid data. It
implements the validation strategy pattern for content integrity checks.

Author:
    Tariq Ahmed (t.ahmed@stride.ae)

Organization:
    Stride Information Technology LLC

Example:
    >>> validator = ContentValidator()
    >>> data = {
    ...     "doc.md": [{
    ...         "title": "Valid Title",
    ...         "content": "Valid content",
    ...         "level": 1,
    ...         "children": [{
    ...             "title": "Subsection",
    ...             "content": "More content",
    ...             "level": 2,
    ...             "children": []
    ...         }]
    ...     }]
    ... }
    >>> is_valid, error = validator.validate(data)
    >>> print("Valid content" if is_valid else f"Invalid: {error}")
"""

from typing import Dict, Any, Tuple, Optional
from .base.base_validator import ValidationStrategy
from .base.error_handler import ValidationError

class ContentValidator(ValidationStrategy):
    """Validates document content values and relationships.

    This validator ensures that document content meets requirements,
    including:
    1. Non-empty titles for all sections
    2. Valid string content for all sections
    3. Proper content in child sections
    4. Valid data types for content fields

    The validator uses the ValidationStrategy pattern and provides detailed
    error messages through the ErrorFormatter for any content violations.

    Attributes:
        error_formatter (ErrorFormatter): Utility for consistent error messages
    """

    def validate(self, data: Dict[str, Any]) -> Tuple[bool, Optional[ValidationError]]:
        """Validate document content values.

        Performs comprehensive content validation, ensuring all sections
        have valid titles and content. This includes checking both
        top-level sections and recursively validating child sections.

        Args:
            data (Dict[str, Any]): Document data to validate, containing:
                - Filename as key
                - List of sections as value, where each section has:
                    - title (str): Non-empty section heading
                    - content (str): Section content text
                    - children (List): List of subsections

        Returns:
            Tuple[bool, Optional[ValidationError]]: A tuple containing:
                - bool: True if content is valid, False otherwise
                - Optional[ValidationError]: Error details if invalid,
                  None if valid

        Example:
            >>> validator = ContentValidator()
            >>> data = {
            ...     "doc.md": [{
            ...         "title": "Test",
            ...         "content": "Valid content",
            ...         "level": 1,
            ...         "children": []
            ...     }]
            ... }
            >>> valid, error = validator.validate(data)
            >>> if not valid:
            ...     print(f"Content error: {error}")
        """
        try:
            for filename, sections in data.items():
                if not isinstance(sections, list):
                    continue

                for section in sections:
                    # Validate title not empty
                    title = section.get('title', '').strip()
                    if not self._check_not_empty(title, f"Title in {filename}"):
                        return False, ValidationError(
                            self.error_formatter.format_empty_error(
                                f"Title in {filename}"
                            )
                        )

                    # Content must be string
                    content = section.get('content', '')
                    if not self._check_type(content, str, f"Content in section '{title}'"):
                        return False, ValidationError(
                            self.error_formatter.format_type_error(
                                content,
                                str,
                                f"Content in section '{title}'"
                            )
                        )

                    # Validate children recursively
                    children = section.get('children', [])
                    if not self._check_type(children, list, f"Children in section '{title}'"):
                        return False, ValidationError(
                            self.error_formatter.format_type_error(
                                children,
                                list,
                                f"Children in section '{title}'"
                            )
                        )

                    for child in children:
                        valid, error = self._validate_section(child, title)
                        if not valid:
                            return False, error

            return True, None
        except Exception as e:
            return False, ValidationError(str(e))

    def _validate_section(self, section: Dict[str, Any], parent: str) -> Tuple[bool, Optional[ValidationError]]:
        """Validate content of an individual section.

        Performs detailed validation of a single section's content,
        including title, content text, and recursive validation of
        child sections.

        Args:
            section (Dict[str, Any]): Section data to validate
            parent (str): Parent section title for context

        Returns:
            Tuple[bool, Optional[ValidationError]]: A tuple containing:
                - bool: True if section content is valid, False otherwise
                - Optional[ValidationError]: Error details if invalid,
                  None if valid

        Example:
            >>> validator = ContentValidator()
            >>> section = {
            ...     "title": "Valid Title",
            ...     "content": "Valid content",
            ...     "level": 1,
            ...     "children": []
            ... }
            >>> valid, error = validator._validate_section(
            ...     section, "Parent Section"
            ... )
        """
        # Title required and not empty
        title = section.get('title', '').strip()
        if not self._check_not_empty(title, f"Title in child section of '{parent}'"):
            return False, ValidationError(
                self.error_formatter.format_empty_error(
                    f"Title in child section of '{parent}'"
                )
            )

        # Content must be string
        content = section.get('content', '')
        if not self._check_type(content, str, f"Content in section '{title}'"):
            return False, ValidationError(
                self.error_formatter.format_type_error(
                    content,
                    str,
                    f"Content in section '{title}'"
                )
            )

        # Validate children recursively
        children = section.get('children', [])
        if not self._check_type(children, list, f"Children in section '{title}'"):
            return False, ValidationError(
                self.error_formatter.format_type_error(
                    children,
                    list,
                    f"Children in section '{title}'"
                )
            )

        for child in children:
            valid, error = self._validate_section(child, title)
            if not valid:
                return False, error

        return True, None
