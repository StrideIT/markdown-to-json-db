"""
Content accumulation module for markdown section content.

This module handles the accumulation of content between markdown headings,
preserving empty lines and formatting while organizing content into logical
blocks based on the document's heading structure.

Author:
    Tariq Ahmed (t.ahmed@stride.ae)

Organization:
    Stride Information Technology LLC

Example:
    >>> accumulator = ContentAccumulator()
    >>> content = [
    ...     "# Title",
    ...     "First paragraph",
    ...     "",
    ...     "Second paragraph",
    ...     "## Section",
    ...     "Section content"
    ... ]
    >>> result = accumulator.handle(content)
    >>> print(len(result["blocks"]))  # 2 content blocks
    2
"""

import re
from typing import Dict, Any, List, Union
from .base_handler import ParserHandler

class ContentAccumulator(ParserHandler):
    """Accumulates and organizes content between markdown headings.

    This handler processes markdown content by identifying and collecting
    text blocks between headings. It maintains the original formatting
    including empty lines while grouping content logically.

    The handler follows these rules:
    1. Preserves empty lines within content blocks
    2. Maintains original line endings
    3. Groups content until the next heading is found
    4. Joins content blocks with newlines
    5. Handles both raw content and partially processed input

    Attributes:
        heading_pattern (re.Pattern): Compiled regex for heading detection
    """

    def handle(self, content: Union[List[str], Dict[str, Any]]) -> Dict[str, Any]:
        """Process content to accumulate text between headings.

        Analyzes the content line by line, accumulating text into blocks
        that are separated by headings. Preserves formatting and empty
        lines within each block while maintaining a clean separation
        between sections.

        Args:
            content (Union[List[str], Dict[str, Any]]): The content to
                process. Can be either:
                - List[str]: Raw markdown lines
                - Dict[str, Any]: Partially processed content with
                  'content' key containing lines

        Returns:
            Dict[str, Any]: A dictionary containing:
                - 'blocks': List[str] where each string is a complete
                  content block between headings, with original formatting
                  preserved

        Example:
            >>> accumulator = ContentAccumulator()
            >>> result = accumulator.handle([
            ...     "# Title",
            ...     "Content here",
            ...     "",
            ...     "More content",
            ...     "## Section"
            ... ])
            >>> print(result["blocks"][0].count("\\n"))  # 2 newlines
            2
        """
        if isinstance(content, dict):
            content = content.get('content', [])
            
        blocks = []
        current_block = []
        
        for line in content:
            if re.match(r'^#{1,6}\s+.+$', line):
                if current_block:
                    blocks.append('\n'.join(current_block))
                    current_block = []
            else:
                # Keep empty lines by appending them even if they're empty
                current_block.append(line.rstrip())
        
        if current_block:
            blocks.append('\n'.join(current_block))
        
        return {'blocks': blocks}
