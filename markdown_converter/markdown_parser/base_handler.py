"""
Base handler module defining the parser component interface.

This module provides the foundational abstract base class that all markdown
parsing components must implement. It defines a consistent interface for
handling different aspects of markdown parsing using the Chain of
Responsibility pattern.

Author:
    Tariq Ahmed (t.ahmed@stride.ae)

Organization:
    Stride Information Technology LLC

Example:
    >>> class HeadingHandler(ParserHandler):
    ...     def handle(self, content):
    ...         # Process headings
    ...         return {"headings": [...]}
    >>> handler = HeadingHandler()
    >>> result = handler.handle(["# Title", "Content"])
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Union, TypeVar

T = TypeVar('T', List[str], Dict[str, Any])

class ParserHandler(ABC):
    """Abstract base class for markdown parsing components.

    This class defines the interface for parser handlers using the Chain
    of Responsibility pattern. Each concrete handler focuses on a specific
    aspect of markdown parsing (e.g., headings, content, structure).

    The handler interface is generic over the content type, allowing
    handlers to work with either raw content (List[str]) or partially
    processed content (Dict[str, Any]).

    Type Variables:
        T: Union[List[str], Dict[str, Any]] - The type of content to handle,
            either raw lines or processed data.
    """

    @abstractmethod
    def handle(self, content: T) -> Dict[str, Any]:
        """Process the provided content according to handler's responsibility.

        This abstract method must be implemented by concrete handlers to
        define their specific parsing logic. Each handler processes its
        assigned aspect of the markdown content and returns the results
        in a dictionary.

        Args:
            content (T): The content to process. Can be either:
                - List[str]: Raw markdown lines
                - Dict[str, Any]: Partially processed content

        Returns:
            Dict[str, Any]: Results of the parsing operation. The exact
                structure depends on the concrete handler's responsibility.

        Raises:
            NotImplementedError: If the concrete class doesn't implement
                this method.

        Example:
            >>> class ContentHandler(ParserHandler):
            ...     def handle(self, content):
            ...         if isinstance(content, list):
            ...             return {"content": "\\n".join(content)}
            ...         return {}
        """
        return {}
