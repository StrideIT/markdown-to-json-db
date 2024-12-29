"""
Database handler module for markdown conversion data persistence.

This module provides a clean interface to the database package by re-exporting
the essential database handling components. It serves as the main entry point
for all database operations in the markdown conversion system.

Author:
    Tariq Ahmed (t.ahmed@stride.ae)

Organization:
    Stride Information Technology LLC

Example:
    >>> handler = DatabaseHandler()
    >>> doc_id = handler.insert_document("example.md")
    >>> handler.insert_json_output(doc_id, {"content": "..."})

Note:
    For detailed documentation of database operations and schema,
    refer to the database package documentation.
"""

from .database import DatabaseHandler, DatabaseError

__all__ = ['DatabaseHandler', 'DatabaseError']
