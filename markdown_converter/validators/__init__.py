"""
Validator package for ensuring data integrity and structure.

This package provides a comprehensive validation system for ensuring the
correctness and consistency of JSON data produced by the markdown conversion
process. It implements a multi-layered validation approach that checks
different aspects of the data.

Author:
    Tariq Ahmed (t.ahmed@stride.ae)

Organization:
    Stride Information Technology LLC

Components:
    - Schema Validation: Ensures correct data structure and types
    - Content Validation: Verifies data values and relationships
    - Structure Validation: Checks hierarchical section organization

Features:
    - Modular validation strategy
    - Detailed error reporting
    - Hierarchical structure verification
    - Type checking and validation
    - Content integrity checks

Example:
    >>> validator = Validator()
    >>> data = {
    ...     "example.md": [{
    ...         "title": "Section",
    ...         "content": "Content",
    ...         "level": 1,
    ...         "children": []
    ...     }]
    ... }
    >>> is_valid, error = validator.validate(data)
    >>> print("Valid" if is_valid else f"Error: {error}")
"""

from typing import Dict, Any, Tuple
from .schema_validator import SchemaValidator
from .content_validator import ContentValidator
from .structure_validator import StructureValidator

class Validator:
    """Main validator class orchestrating the validation process.

    This class coordinates multiple validation strategies to ensure data
    integrity across different aspects of the document structure. It applies
    validators in a specific order: schema, content, and structure, failing
    fast if any validation step fails.

    The validation process is comprehensive, checking:
    1. Schema: Correct data types and required fields
    2. Content: Valid values and relationships
    3. Structure: Proper hierarchical organization

    Attributes:
        schema_validator (SchemaValidator): Validates data structure
        content_validator (ContentValidator): Validates content values
        structure_validator (StructureValidator): Validates hierarchy
    """

    def __init__(self):
        """Initialize validators."""
        self.schema_validator = SchemaValidator()
        self.content_validator = ContentValidator()
        self.structure_validator = StructureValidator()

    def validate(self, data: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate data through all validation stages.

        Processes the data through each validator in sequence, stopping at
        the first validation failure. The validation order is important as
        each stage builds on the assumptions of the previous stage.

        Args:
            data (Dict[str, Any]): The data structure to validate. Should
                be a dictionary with filename keys and section list values.

        Returns:
            Tuple[bool, str]: A tuple containing:
                - bool: True if all validations pass, False otherwise
                - str: Error message if validation fails, empty string if passes

        Example:
            >>> validator = Validator()
            >>> data = {"file.md": [{"title": "Test", "level": 1}]}
            >>> valid, error = validator.validate(data)
            >>> if not valid:
            ...     print(f"Validation failed: {error}")
        """
        # Schema validation
        valid, error = self.schema_validator.validate(data)
        if not valid:
            return False, f"Schema validation failed: {error}"

        # Content validation
        valid, error = self.content_validator.validate(data)
        if not valid:
            return False, f"Content validation failed: {error}"

        # Structure validation
        valid, error = self.structure_validator.validate(data)
        if not valid:
            return False, f"Structure validation failed: {error}"

        return True, ""

# Export classes
__all__ = ['Validator']
