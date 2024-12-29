"""
Tree structure management module for markdown document hierarchy.

This module handles the construction of a hierarchical tree structure from
markdown headings and content blocks. It maintains proper section nesting
based on heading levels while associating content with appropriate sections.

Author:
    Tariq Ahmed (t.ahmed@stride.ae)

Organization:
    Stride Information Technology LLC

Example:
    >>> manager = TreeManager()
    >>> content = {
    ...     "headings": [
    ...         {"title": "Main", "level": 1},
    ...         {"title": "Sub", "level": 2}
    ...     ],
    ...     "blocks": ["Main content", "Sub content"]
    ... }
    >>> result = manager.handle(content)
    >>> tree = result["tree"]
    >>> print(tree[0]["title"], len(tree[0]["children"]))
    Main 1
"""

from typing import Dict, Any, List
from .base_handler import ParserHandler

class TreeManager(ParserHandler):
    """Manages the hierarchical document tree structure.

    This handler processes heading and content information to build a
    properly nested tree structure representing the document's organization.
    It maintains section relationships based on heading levels while
    associating content blocks with their respective sections.

    The handler follows these rules:
    1. Creates a tree based on heading levels (1-6)
    2. Maintains proper parent-child relationships
    3. Associates content blocks with sections
    4. Handles nested sections of any depth
    5. Preserves section order and hierarchy

    The resulting tree structure can be traversed to understand the
    document's organization and access section content efficiently.
    """

    def handle(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Build a hierarchical tree from headings and content blocks.

        Processes heading and content information to create a nested tree
        structure that represents the document's organization. Uses a stack
        to maintain proper section nesting based on heading levels.

        Args:
            content (Dict[str, Any]): Dictionary containing:
                - headings: List of heading dictionaries with:
                    - title: str
                    - level: int (1-6)
                - blocks: List of content strings

        Returns:
            Dict[str, Any]: A dictionary containing:
                - 'tree': List[Dict[str, Any]] where each dict is a
                  section node with:
                    - title: str
                    - content: str
                    - level: int
                    - children: List[Dict[str, Any]]

        Example:
            >>> manager = TreeManager()
            >>> result = manager.handle({
            ...     "headings": [
            ...         {"title": "H1", "level": 1},
            ...         {"title": "H2", "level": 2}
            ...     ],
            ...     "blocks": ["Content 1", "Content 2"]
            ... })
            >>> print(result["tree"][0]["children"][0]["title"])
            H2
        """
        if not isinstance(content, dict):
            return {'tree': []}
            
        headings = content.get('headings', [])
        blocks = content.get('blocks', [])
        
        root: List[Dict[str, Any]] = []
        stack: List[Dict[str, Any]] = []
        current_content_index = 0

        for heading in headings:
            while stack and stack[-1]['level'] >= heading['level']:
                stack.pop()

            # Get section content
            section_content = ''
            if current_content_index < len(blocks):
                section_content = blocks[current_content_index]
                current_content_index += 1

            node = {
                'title': heading['title'],
                'content': section_content,
                'level': heading['level'],
                'children': []
            }

            if not stack:
                root.append(node)
            else:
                stack[-1]['children'].append(node)
            
            stack.append(node)

        return {'tree': root}
