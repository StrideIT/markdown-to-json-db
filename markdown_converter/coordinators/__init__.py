"""
Coordinator components package for managing conversion operations.

This package provides specialized coordinators that handle different aspects
of the markdown to JSON conversion process. Each coordinator is responsible
for a specific domain of operations, following the Single Responsibility
Principle.

Author:
    Tariq Ahmed (t.ahmed@stride.ae)

Organization:
    Stride Information Technology LLC

Components:
    - FileOperationsCoordinator: Handles all file I/O operations
    - ConversionCoordinator: Manages the markdown to JSON conversion process
    - DatabaseOperationsCoordinator: Handles database storage operations

Example:
    >>> file_coord = FileOperationsCoordinator("input.md")
    >>> content = file_coord.read_content()
    >>> conv_coord = ConversionCoordinator("input.md")
    >>> data = conv_coord.convert(content)
    >>> db_coord = DatabaseOperationsCoordinator()
    >>> db_coord.save("input.md", data)
"""

from .file_operations import FileOperationsCoordinator
from .conversion import ConversionCoordinator
from .database_operations import DatabaseOperationsCoordinator

__all__ = [
    'FileOperationsCoordinator',
    'ConversionCoordinator',
    'DatabaseOperationsCoordinator'
]
