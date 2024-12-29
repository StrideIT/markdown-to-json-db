"""
Base validator module defining the validation strategy interface.

This module provides the foundational abstract base class that all validation
strategies must implement. It defines a consistent interface and provides common
utility methods for type checking, emptiness validation, and field existence
verification.

Author:
    Tariq Ahmed (t.ahmed@stride.ae)

Organization:
    Stride Information Technology LLC

Example:
    >>> class CustomValidator(ValidationStrategy):
    ...     def validate(self, data):
    ...         try:
    ...             self._check_type(data, dict, "Root data")
    ...             self._check_not_empty(data, "Root data")
    ...             return True, None
    ...         except ValidationError as e:
    ...             return False, e
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple, Optional
from .error_handler import ValidationError, ErrorFormatter

class ValidationStrategy(ABC):
    """Abstract base class defining the validation strategy interface.

    This class provides a template for implementing validation strategies
    using the Strategy pattern. Each concrete validator implements its own
    validation logic while inheriting common utility methods for type
    checking and error handling.

    The class uses composition with ErrorFormatter for consistent error
    message formatting across all validation strategies.

    Attributes:
        error_formatter (ErrorFormatter): Utility for formatting error messages
            in a consistent way across all validators.
    """

    def __init__(self):
        """Initialize the validation strategy."""
        self.error_formatter = ErrorFormatter()

    @abstractmethod
    def validate(self, data: Dict[str, Any]) -> Tuple[bool, Optional[ValidationError]]:
        """Validate data according to the strategy's specific rules.

        This abstract method must be implemented by concrete validator classes
        to define their specific validation logic. The implementation should
        use the utility methods provided by this base class for consistent
        error handling.

        Args:
            data (Dict[str, Any]): The data structure to validate. The exact
                schema requirements depend on the concrete validator.

        Returns:
            Tuple[bool, Optional[ValidationError]]: A tuple containing:
                - bool: True if validation passed, False otherwise
                - Optional[ValidationError]: Detailed error information if
                    validation failed, None if validation passed

        Raises:
            NotImplementedError: If the concrete class doesn't implement this method

        Example:
            >>> class SimpleValidator(ValidationStrategy):
            ...     def validate(self, data):
            ...         try:
            ...             self._check_type(data, dict, "Data")
            ...             return True, None
            ...         except ValidationError as e:
            ...             return False, e
        """
        pass

    def _check_type(self, value: Any, expected_type: type, context: str) -> bool:
        """Check if a value matches the expected type.

        Performs type validation using isinstance() to support inheritance
        hierarchies. Raises a formatted error if the type check fails.

        Args:
            value (Any): The value to check. Can be of any type.
            expected_type (type): The expected Python type.
            context (str): Description of the value being checked, used
                in error messages.

        Returns:
            bool: True if the type matches. Never returns False as it
                raises an exception for type mismatches.

        Raises:
            ValidationError: If the value is not of the expected type.
                The error message includes the context, actual type,
                and expected type.

        Example:
            >>> validator = ConcreteValidator()
            >>> try:
            ...     validator._check_type(42, str, "User ID")
            ... except ValidationError as e:
            ...     print(e)  # "User ID must be a str, got int instead"
        """
        if not isinstance(value, expected_type):
            raise ValidationError(
                self.error_formatter.format_type_error(value, expected_type, context)
            )
        return True

    def _check_not_empty(self, value: Any, context: str) -> bool:
        """Verify that a value is not empty.

        Checks for emptiness using Python's truthiness rules. This means
        it will consider the following as empty:
        - Empty strings, lists, dicts, sets, etc.
        - None
        - False
        - Zero (0)

        Args:
            value (Any): The value to check for emptiness.
            context (str): Description of the value being checked, used
                in error messages.

        Returns:
            bool: True if the value is not empty. Never returns False as
                it raises an exception for empty values.

        Raises:
            ValidationError: If the value is considered empty according to
                Python's truthiness rules.

        Example:
            >>> validator = ConcreteValidator()
            >>> try:
            ...     validator._check_not_empty("", "Username")
            ... except ValidationError as e:
            ...     print(e)  # "Username cannot be empty"
        """
        if not value:
            raise ValidationError(
                self.error_formatter.format_empty_error(context)
            )
        return True

    def _check_field_exists(self, data: Dict[str, Any], field: str, context: str) -> bool:
        """Verify that a required field exists in a dictionary.

        Checks for the existence of a field in a dictionary using the 'in'
        operator. This ensures the field exists regardless of its value
        (which might be None or empty).

        Args:
            data (Dict[str, Any]): The dictionary to check.
            field (str): The name of the required field.
            context (str): Description of the data structure being checked,
                used in error messages.

        Returns:
            bool: True if the field exists. Never returns False as it
                raises an exception for missing fields.

        Raises:
            ValidationError: If the specified field is not present in
                the dictionary.

        Example:
            >>> validator = ConcreteValidator()
            >>> data = {"name": "John"}
            >>> try:
            ...     validator._check_field_exists(data, "age", "User")
            ... except ValidationError as e:
            ...     print(e)  # "Missing required field 'age' in User"
        """
        if field not in data:
            raise ValidationError(
                self.error_formatter.format_missing_field_error(field, context)
            )
        return True
