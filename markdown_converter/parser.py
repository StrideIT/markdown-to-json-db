"""
Markdown parser module for converting markdown to structured JSON.

This module provides the core functionality for parsing markdown content into
a structured JSON format. It uses a chain of specialized handlers to process
different aspects of the markdown content, including heading detection,
content accumulation, and tree structure management.

Author:
    Tariq Ahmed (t.ahmed@stride.ae)

Organization:
    Stride Information Technology LLC

Example:
    >>> parser = MarkdownParser("example.md")
    >>> content = ["# Title", "", "Content here"]
    >>> result = parser.parse(content)
    >>> "example.md" in result
    True
"""

import os
from typing import Dict, Any, List
from .markdown_parser.heading_detector import HeadingDetector
from .markdown_parser.content_accumulator import ContentAccumulator
from .markdown_parser.tree_manager import TreeManager

class MarkdownParser:
    """Main parser class that coordinates the markdown parsing process.

    This class manages a chain of specialized handlers that process markdown
    content in sequence. Each handler focuses on a specific aspect of parsing:
    1. HeadingDetector: Identifies and processes markdown headings
    2. ContentAccumulator: Collects and organizes content between headings
    3. TreeManager: Builds a hierarchical structure from the parsed content

    Attributes:
        source_file (str): Path to the source markdown file being parsed.
        handlers (List[ParserHandler]): List of parsing handlers in execution order.
    """

    def __init__(self, source_file: str) -> None:
        """Initialize the MarkdownParser with a source file.

        Sets up the parser with a chain of specialized handlers for processing
        different aspects of the markdown content. The handlers are executed
        in sequence during the parsing process.

        Args:
            source_file (str): Path to the source markdown file. This is used
                primarily for generating the output structure's key.

        Example:
            >>> parser = MarkdownParser("doc.md")
            >>> isinstance(parser.handlers[0], HeadingDetector)
            True
        """
        self.source_file = source_file
        self.handlers = [
            HeadingDetector(),
            ContentAccumulator(),
            TreeManager()
        ]

    def parse(self, content: List[str]) -> Dict[str, Any]:
        """Parse Markdown content into structured JSON format.

        Processes the markdown content through each handler in sequence,
        building up a structured representation of the document. The final
        output is wrapped in a dictionary keyed by the source filename.

        Args:
            content (List[str]): The markdown content to parse. Each string
                in the list represents one line from the source file.

        Returns:
            Dict[str, Any]: A structured representation of the document where:
                - The top level key is the source filename
                - The value is a list containing the root section
                - Each section has title, content, level, and children fields

        Example:
            >>> parser = MarkdownParser("test.md")
            >>> result = parser.parse(["# Title", "", "Content"])
            >>> result["test.md"][0]["title"] == "Title"
            True
        """
        parsed_content: Dict[str, Any] = {'content': content}
        
        for handler in self.handlers:
            result = handler.handle(parsed_content)
            parsed_content.update(result)

        tree = parsed_content.get('tree', [])
        if not tree:
            return {
                os.path.basename(self.source_file): [{
                    'title': "Document",
                    'content': "",
                    'level': 1,
                    'children': []
                }]
            }

        first_node = tree[0]
        return {
            os.path.basename(self.source_file): [{
                'title': first_node.get('title', "Document"),
                'content': first_node.get('content', ""),
                'level': 1,
                'children': first_node.get('children', [])
            }]
        }
