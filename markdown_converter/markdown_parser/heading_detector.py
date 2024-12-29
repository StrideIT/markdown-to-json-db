"""
Heading detection module for markdown section analysis.

This module provides functionality to detect and process markdown headings,
identifying their levels and titles. It supports standard markdown heading
syntax with up to 6 levels of headings using '#' characters.

Author:
    Tariq Ahmed (t.ahmed@stride.ae)

Organization:
    Stride Information Technology LLC

Example:
    >>> detector = HeadingDetector()
    >>> content = [
    ...     "# Main Title",
    ...     "Some content",
    ...     "## Subsection",
    ...     "More content"
    ... ]
    >>> result = detector.handle(content)
    >>> print(len(result["headings"]))  # 2 headings detected
    2
"""

import re
from typing import Dict, Any, List, Union
from .base_handler import ParserHandler

class HeadingDetector(ParserHandler):
    """Detects and processes markdown heading structures.

    This handler identifies markdown headings using the standard '#' syntax,
    extracting their level (1-6) and title text. It supports both raw
    content processing and working with partially processed content.

    The handler follows these rules:
    1. Recognizes headings with 1-6 '#' characters
    2. Requires space after '#' characters
    3. Captures the entire remaining line as title
    4. Ignores empty lines and non-heading content

    Attributes:
        heading_pattern (re.Pattern): Compiled regex for heading detection
    """

    def handle(self, content: Union[List[str], Dict[str, Any]]) -> Dict[str, Any]:
        """Process content to detect and extract heading information.

        Analyzes the provided content line by line to identify markdown
        headings. For each heading found, extracts its level (based on
        number of '#' characters) and title text.

        Args:
            content (Union[List[str], Dict[str, Any]]): The content to
                process. Can be either:
                - List[str]: Raw markdown lines
                - Dict[str, Any]: Partially processed content with
                  'content' key containing lines

        Returns:
            Dict[str, Any]: A dictionary containing:
                - 'headings': List of detected headings, each with:
                    - 'level': int (1-6)
                    - 'title': str
                    - 'content': str (empty initially)

        Example:
            >>> detector = HeadingDetector()
            >>> result = detector.handle(["# Title", "## Section"])
            >>> headings = result["headings"]
            >>> print(f"Level {headings[0]['level']}: {headings[0]['title']}")
            Level 1: Title
        """
        if isinstance(content, dict):
            content = content.get('content', [])
            
        headings = []
        for line in content:
            line = line.strip()
            if not line:
                continue
            heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if heading_match:
                headings.append({
                    'level': len(heading_match.group(1)),
                    'title': heading_match.group(2),
                    'content': ''
                })
        return {'headings': headings}
