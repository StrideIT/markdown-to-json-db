"""
Validator module for ensuring JSON data structure integrity.

This module provides a clean interface to the validators package by re-exporting
the main Validator class. It serves as the central entry point for all validation
operations in the markdown conversion system, ensuring data consistency and
structural integrity.

Author:
    Tariq Ahmed (t.ahmed@stride.ae)

Organization:
    Stride Information Technology LLC

Example:
    >>> validator = Validator()
    >>> data = {"file.md": [{"title": "Section", "content": "", "level": 1}]}
    >>> is_valid, error = validator.validate(data)
    >>> print("Valid" if is_valid else f"Error: {error}")

Note:
    For detailed documentation of validation rules and strategies,
    refer to the validators package documentation.
"""

from .validators import Validator

__all__ = ['Validator']
