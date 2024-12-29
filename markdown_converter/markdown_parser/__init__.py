"""
Markdown parsing package for structured content analysis.

This package provides specialized components for parsing markdown content into
a structured format. It implements a chain of responsibility pattern where each
handler focuses on a specific aspect of markdown parsing.

Author:
    Tariq Ahmed (t.ahmed@stride.ae)

Organization:
    Stride Information Technology LLC

Components:
    - ParserHandler: Base class defining the parsing interface
    - HeadingDetector: Identifies and processes markdown headings
    - ContentAccumulator: Collects and organizes content between headings
    - TreeManager: Builds hierarchical structure from parsed content

Example:
    >>> handlers = [
    ...     HeadingDetector(),
    ...     ContentAccumulator(),
    ...     TreeManager()
    ... ]
    >>> content = {"content": ["# Title", "", "Content here"]}
    >>> for handler in handlers:
    ...     result = handler.handle(content)
    ...     content.update(result)
"""

from .base_handler import ParserHandler
from .heading_detector import HeadingDetector
from .content_accumulator import ContentAccumulator
from .tree_manager import TreeManager

__all__ = [
    'ParserHandler',
    'HeadingDetector',
    'ContentAccumulator',
    'TreeManager'
]
