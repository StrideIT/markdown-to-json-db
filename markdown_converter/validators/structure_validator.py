"""
Structure validator module for hierarchical document validation.

This module provides validation for document section hierarchies, ensuring
proper nesting and level relationships between sections. It implements
the validation strategy pattern for structural integrity checks.

Author:
    Tariq Ahmed (t.ahmed@stride.ae)

Organization:
    Stride Information Technology LLC

Example:
    >>> validator = StructureValidator()
    >>> data = {
    ...     "doc.md": [{
    ...         "title": "Section 1",
    ...         "level": 1,
    ...         "children": [{
    ...             "title": "Section 1.1",
    ...             "level": 2,
    ...             "children": []
    ...         }]
    ...     }]
    ... }
    >>> is_valid, error = validator.validate(data)
    >>> print("Valid structure" if is_valid else f"Invalid: {error}")
"""

from typing import Dict, Any, Tuple, List, Optional
from .base.base_validator import ValidationStrategy
from .base.error_handler import ValidationError

class StructureValidator(ValidationStrategy):
    """Validates document section hierarchy and relationships.

    This validator ensures that document sections follow proper hierarchical
    rules, including:
    1. Section levels increase by at most 1 at a time
    2. Child sections have higher levels than their parents
    3. All sections maintain proper parent-child relationships

    The validator uses the ValidationStrategy pattern and provides detailed
    error messages through the ErrorFormatter for any structural issues.

    Attributes:
        error_formatter (ErrorFormatter): Utility for consistent error messages
    """

    def validate(self, data: Dict[str, Any]) -> Tuple[bool, Optional[ValidationError]]:
        """Validate the hierarchical structure of document sections.

        Performs comprehensive validation of section hierarchy, ensuring
        proper nesting and level relationships between sections. This includes
        checking level transitions and parent-child relationships.

        Args:
            data (Dict[str, Any]): Document data to validate, containing:
                - Filename as key
                - List of sections as value, where each section has:
                    - title: Section heading
                    - level: Section level (1-6)
                    - children: List of subsections

        Returns:
            Tuple[bool, Optional[ValidationError]]: A tuple containing:
                - bool: True if structure is valid, False otherwise
                - Optional[ValidationError]: Error details if invalid,
                  None if valid

        Example:
            >>> validator = StructureValidator()
            >>> data = {
            ...     "doc.md": [{
            ...         "title": "H1",
            ...         "level": 1,
            ...         "children": [{
            ...             "title": "H2",
            ...             "level": 2,
            ...             "children": []
            ...         }]
            ...     }]
            ... }
            >>> valid, error = validator.validate(data)
            >>> if not valid:
            ...     print(f"Structure error: {error}")
        """
        try:
            for filename, sections in data.items():
                if not isinstance(sections, list):
                    continue

                # Track section levels
                current_level = 0
                for section in sections:
                    level = section.get('level', 0)
                    
                    # Level can't decrease by more than 1
                    if level > current_level + 1:
                        return False, ValidationError(
                            self.error_formatter.format_structure_error(
                                filename,
                                f"Invalid section level jump in {section['title']}"
                            )
                        )
                    
                    # Validate children
                    valid, error = self._validate_children(section, filename, level)
                    if not valid:
                        return False, error
                    
                    current_level = level

            return True, None
        except Exception as e:
            return False, ValidationError(str(e))

    def _validate_children(self, section: Dict[str, Any], context: str, parent_level: int) -> Tuple[bool, Optional[ValidationError]]:
        """Validate hierarchical relationships of section children.
        
        Recursively validates the structure of section children, ensuring
        proper level progression and parent-child relationships throughout
        the section tree.

        Args:
            section (Dict[str, Any]): Section to validate, containing:
                - title: Section heading
                - level: Section level (1-6)
                - children: List of subsections
            context (str): Document/section context for error messages
            parent_level (int): Level of the parent section

        Returns:
            Tuple[bool, Optional[ValidationError]]: A tuple containing:
                - bool: True if children are valid, False otherwise
                - Optional[ValidationError]: Error details if invalid,
                  None if valid

        Example:
            >>> validator = StructureValidator()
            >>> section = {
            ...     "title": "Parent",
            ...     "level": 1,
            ...     "children": [{
            ...         "title": "Child",
            ...         "level": 2,
            ...         "children": []
            ...     }]
            ... }
            >>> valid, error = validator._validate_children(
            ...     section, "doc.md", 1
            ... )
        """
        if not isinstance(section.get('children'), list):
            return True, None

        for child in section['children']:
            if not isinstance(child, dict):
                return False, ValidationError(
                    self.error_formatter.format_type_error(
                        child,
                        dict,
                        f"Child section in {context}"
                    )
                )

            child_level = child.get('level', 0)
            if child_level <= parent_level:
                return False, ValidationError(
                    self.error_formatter.format_structure_error(
                        context,
                        f"Child level must be greater than parent level"
                    )
                )

            # Recursively validate child's children
            valid, error = self._validate_children(child, context, child_level)
            if not valid:
                return False, error

        return True, None
