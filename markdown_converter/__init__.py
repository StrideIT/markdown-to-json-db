"""
Markdown to JSON converter package with database integration.

This package provides a comprehensive solution for converting markdown files
to structured JSON format with optional database persistence. It handles the
complete conversion pipeline including file operations, content parsing,
validation, and data storage.

Author:
    Tariq Ahmed (t.ahmed@stride.ae)

Organization:
    Stride Information Technology LLC

Features:
    - Markdown to JSON conversion with hierarchical structure preservation
    - Flexible output options (file system and/or database storage)
    - Robust validation of converted data
    - Cross-platform compatibility
    - UTF-8 encoding support

Example:
    >>> from markdown_converter import MarkdownConverter
    >>> converter = MarkdownConverter("document.md", save_to_db=True)
    >>> output_path = converter.convert()
    >>> print(f"Conversion complete: {output_path}")

Version: 1.0.0
"""

from .markdown_converter import MarkdownConverter

__all__ = ['MarkdownConverter']
