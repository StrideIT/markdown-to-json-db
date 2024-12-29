"""
Error handling module for consistent validation error management.

This module provides specialized error handling and message formatting for
validation errors. It ensures consistent error reporting across all validation
operations through standardized error types and message formats.

Author:
    Tariq Ahmed (t.ahmed@stride.ae)

Organization:
    Stride Information Technology LLC

Example:
    >>> formatter = ErrorFormatter()
    >>> try:
    ...     value = 42
    ...     if not isinstance(value, str):
    ...         msg = formatter.format_type_error(value, str, "Username")
    ...         raise ValidationError(msg)
    ... except ValidationError as e:
    ...     print(e)  # "Username must be a str, got int instead"
"""

from typing import Any

class ValidationError(Exception):
    """Custom exception class for validation-specific errors.

    This exception class is used to distinguish validation errors from other
    types of errors that might occur during the conversion process. It
    provides a clean way to catch and handle validation-specific issues.

    Attributes:
        message (str): Detailed error message explaining the validation failure
    """
    
    def __init__(self, message: str):
        """
        Initialize ValidationError.

        Args:
            message (str): Error message
        """
        self.message = message
        super().__init__(self.message)

class ErrorFormatter:
    """Utility class for formatting validation error messages.

    This class provides a collection of methods for generating consistently
    formatted error messages for different types of validation failures.
    Each method focuses on a specific type of error (type mismatch,
    missing field, etc.) and generates an appropriate error message.

    The formatted messages are designed to be:
    - Clear and concise
    - Consistent in structure
    - Informative for debugging
    - User-friendly for error reporting
    """

    def format_type_error(self, value: Any, expected_type: type, context: str) -> str:
        """Format error message for type validation failures.

        Creates a formatted error message when a value's type doesn't match
        the expected type. The message includes the context, expected type,
        and actual type for clear error reporting.

        Args:
            value (Any): The value that failed type validation.
            expected_type (type): The type that was expected.
            context (str): Description of where the error occurred.

        Returns:
            str: A formatted error message describing the type mismatch.

        Example:
            >>> formatter = ErrorFormatter()
            >>> msg = formatter.format_type_error(42, str, "Username")
            >>> print(msg)
            "Username must be a str, got int instead"
        """
        return (
            f"{context} must be a {expected_type.__name__}, "
            f"got {type(value).__name__} instead"
        )

    def format_empty_error(self, context: str) -> str:
        """Format error message for empty value validation failures.

        Creates a formatted error message when a required value is empty.
        This applies to strings, lists, dictionaries, or any other
        container type that can be empty.

        Args:
            context (str): Description of the empty value's context.

        Returns:
            str: A formatted error message about the empty value.

        Example:
            >>> formatter = ErrorFormatter()
            >>> msg = formatter.format_empty_error("Title")
            >>> print(msg)
            "Title cannot be empty"
        """
        return f"{context} cannot be empty"

    def format_missing_field_error(self, field: str, context: str) -> str:
        """Format error message for missing required fields.

        Creates a formatted error message when a required field is missing
        from a data structure. This is typically used when validating
        dictionary structures.

        Args:
            field (str): Name of the missing required field.
            context (str): Description of the data structure context.

        Returns:
            str: A formatted error message about the missing field.

        Example:
            >>> formatter = ErrorFormatter()
            >>> msg = formatter.format_missing_field_error("email", "User")
            >>> print(msg)
            "Missing required field 'email' in User"
        """
        return f"Missing required field '{field}' in {context}"

    def format_invalid_value_error(self, value: Any, context: str, reason: str) -> str:
        """Format error message for invalid value validation failures.

        Creates a formatted error message when a value is invalid for
        reasons other than type or emptiness (e.g., out of range,
        invalid format, etc.).

        Args:
            value (Any): The invalid value.
            context (str): Description of the value's context.
            reason (str): Explanation of why the value is invalid.

        Returns:
            str: A formatted error message about the invalid value.

        Example:
            >>> formatter = ErrorFormatter()
            >>> msg = formatter.format_invalid_value_error(
            ...     -1, "Age", "must be positive"
            ... )
            >>> print(msg)
            "Invalid value '-1' in Age: must be positive"
        """
        return f"Invalid value '{value}' in {context}: {reason}"

    def format_structure_error(self, context: str, details: str) -> str:
        """Format error message for structural validation failures.

        Creates a formatted error message when the structure of the data
        is invalid (e.g., incorrect nesting, invalid relationships between
        elements, etc.).

        Args:
            context (str): Description of the structure context.
            details (str): Specific details about what's wrong with
                the structure.

        Returns:
            str: A formatted error message about the structural issue.

        Example:
            >>> formatter = ErrorFormatter()
            >>> msg = formatter.format_structure_error(
            ...     "Document", "Section level cannot decrease by more than 1"
            ... )
            >>> print(msg)
            "Invalid structure in Document: Section level cannot decrease by more than 1"
        """
        return f"Invalid structure in {context}: {details}"
