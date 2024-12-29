"""
Schema validation package for JSON structure verification.

This package provides schema validation functionality through the main
SchemaValidator class located in the parent validators directory. This
package exists for organizational purposes and potential future schema
validation extensions.

Author:
    Tariq Ahmed (t.ahmed@stride.ae)

Organization:
    Stride Information Technology LLC

Note:
    The main schema validation functionality is implemented in
    markdown_converter.validators.schema_validator.SchemaValidator.
"""

# Schema validation is implemented in the parent validators directory
from ..schema_validator import SchemaValidator

__all__ = ['SchemaValidator']
