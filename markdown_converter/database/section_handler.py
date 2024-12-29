"""
Section handler module for document section management.

This module provides specialized functionality for managing document sections
in the database, including their hierarchical relationships, content, and
ordering. It handles both storage and retrieval of section data while
maintaining proper parent-child relationships.

Author:
    Tariq Ahmed (t.ahmed@stride.ae)

Organization:
    Stride Information Technology LLC

Example:
    >>> handler = SectionHandler()
    >>> try:
    ...     section_id = handler.insert_section(1, None, {
    ...         "title": "Main Section",
    ...         "content": "Content here",
    ...         "level": 1,
    ...         "children": []
    ...     })
    ...     sections = handler.get_sections(1)
    ...     print(f"Created section {section_id}")
    ... finally:
    ...     handler.close()
"""

from typing import List, Tuple, Dict, Any, Optional
from .base_handler import BaseHandler, DatabaseError

class SectionHandler(BaseHandler):
    """Handles document section management in the database.

    This handler manages the SECTION table, providing operations for
    creating and retrieving document sections. It maintains section
    hierarchies, content, and ordering while ensuring proper relationships
    between sections and their parent documents.

    The handler ensures:
    1. Proper section hierarchy maintenance
    2. Correct section ordering within each level
    3. Content storage and retrieval
    4. Parent-child relationship tracking
    5. Recursive handling of nested sections

    Attributes:
        Inherits connection management from BaseHandler
    """

    def get_sections(self, document_id: int) -> List[Tuple[int, Optional[int], str, str, int]]:
        """Retrieve all sections for a specific document.

        Fetches all sections associated with a document, including their
        hierarchical relationships and content. Results are ordered by
        section ID to maintain proper sequence.

        Args:
            document_id (int): Unique identifier of the document whose
                sections should be retrieved.

        Returns:
            List[Tuple[int, Optional[int], str, str, int]]: List of
                section records, each containing:
                - int: Section ID
                - Optional[int]: Parent section ID (None for root sections)
                - str: Section title
                - str: Section content
                - int: Section level (1-6)

        Example:
            >>> handler = SectionHandler()
            >>> sections = handler.get_sections(1)
            >>> for section in sections:
            ...     level = section[4]
            ...     title = section[2]
            ...     print(f"{'  ' * (level-1)}- {title}")
        """
        return self._execute_query("""
            SELECT id, parent_id, title, content, level 
            FROM SECTION 
            WHERE document_id = %s
            ORDER BY id
        """, (document_id,)) or []

    def insert_section(self, document_id: int, parent_id: Optional[int], section_data: Dict[str, Any]) -> int:
        """Create a new section record with proper hierarchy.

        Creates a new section in the database, handling its position in
        the document hierarchy and recursively processing any child
        sections. Maintains proper ordering of sections within each level.

        Args:
            document_id (int): Unique identifier of the document this
                section belongs to.
            parent_id (Optional[int]): ID of the parent section, or None
                if this is a top-level section.
            section_data (Dict[str, Any]): Section information including:
                - title (str): Section heading text
                - content (str): Section content text
                - level (int): Section level (1-6)
                - children (List[Dict]): Child sections to process

        Returns:
            int: The unique identifier of the created section.

        Raises:
            DatabaseError: If section creation fails or if required data
                is missing/invalid.

        Example:
            >>> handler = SectionHandler()
            >>> section = {
            ...     "title": "Introduction",
            ...     "content": "Chapter content...",
            ...     "level": 1,
            ...     "children": [
            ...         {"title": "Background", "level": 2, "content": "..."}
            ...     ]
            ... }
            >>> section_id = handler.insert_section(1, None, section)
            >>> print(f"Created section tree starting at {section_id}")
        """
        try:
            # Debug print section data
            print(f"Section data: {section_data}")
            print(f"Content type: {type(section_data.get('content', ''))}")
            print(f"Content length: {len(section_data.get('content', ''))}")
            print(f"Content preview: {section_data.get('content', '')[:100]}")
            
            # Debug print
            print(f"Inserting section with content: {section_data.get('content', '')[:100]}")
            
            result = self._execute_query("""
                INSERT INTO SECTION (document_id, parent_id, title, content, level, position)
                VALUES (%s, %s, %s, %s, %s, COALESCE((
                    SELECT MAX(position) + 1
                    FROM SECTION
                    WHERE document_id = %s AND COALESCE(parent_id, 0) = COALESCE(%s, 0)
                ), 1))
                RETURNING id
            """, (
                document_id,
                parent_id,
                section_data['title'],
                section_data.get('content', '').strip(),  # Get content and strip whitespace
                section_data['level'],
                document_id,
                parent_id
            ))
            if not result:
                raise DatabaseError("Failed to insert section")
            section_id = result[0]
            print(f"Inserted section with ID: {section_id} for document ID: {document_id}")

            # Insert child sections recursively
            if 'children' in section_data:
                print(f"Inserting children for section ID: {section_id}")
                for child in section_data['children']:
                    print(f"Inserting child section: {child['title']}")
                    self.insert_section(document_id, section_id, child)

            return section_id
        except DatabaseError as e:
            if "duplicate key" in str(e).lower():
                result = self._execute_query("""
                    SELECT id FROM SECTION 
                    WHERE document_id = %s AND title = %s AND level = %s
                """, (document_id, section_data['title'], section_data['level']))
                if not result:
                    raise DatabaseError("Failed to find existing section")
                section_id = result[0][0]
                print(f"Section already exists with ID: {section_id} for document ID: {document_id}")
                return section_id
            raise
