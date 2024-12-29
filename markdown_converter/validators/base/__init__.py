"""
Base validator package providing core validation functionality.

This package contains the base validation classes and utilities used by all validators.
"""

from .base_validator import ValidationStrategy
from .error_handler import ValidationError, ErrorFormatter

__all__ = ['ValidationStrategy', 'ValidationError', 'ErrorFormatter']
