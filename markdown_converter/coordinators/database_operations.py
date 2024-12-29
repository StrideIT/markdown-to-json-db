"""
Database operations coordinator module for persistent data storage.

This module provides a high-level interface for database operations,
coordinating the storage and retrieval of documents, sections, and
validation results. It ensures proper data persistence and maintains
referential integrity across different database tables.

Author:
    Tariq Ahmed (t.ahmed@stride.ae)

Organization:
    Stride Information Technology LLC

Example:
    >>> coordinator = DatabaseOperationsCoordinator()
    >>> doc_id = coordinator.save("example.md", {
    ...     "example.md": [{
    ...         "title": "Section",
    ...         "content": "Content",
    ...         "level": 1,
    ...         "children": []
    ...     }]
    ... })
    >>> output = coordinator.get_json_output(doc_id)
    >>> print(output is not None)
    True
"""

from typing import Dict, Any, Optional, Tuple
from ..database_handler import DatabaseHandler

class DatabaseOperationsCoordinator:
    """Coordinates database operations for markdown conversion results.

    This class manages all database interactions, providing a high-level
    interface for storing and retrieving conversion results. It handles
    the complexity of maintaining relationships between documents,
    sections, and validation results.

    The coordinator ensures:
    1. Proper document registration and tracking
    2. Hierarchical section storage
    3. JSON output persistence
    4. Validation result recording

    Attributes:
        db_handler (DatabaseHandler): Handles low-level database operations
    """

    def __init__(self):
        """Initialize the DatabaseOperationsCoordinator."""
        self.db_handler = DatabaseHandler()

    def save(self, source_file: str, data: Dict[str, Any]) -> int:
        """Save converted markdown data to the database.

        Performs a complete save operation that includes:
        1. Creating a document record
        2. Storing the JSON output
        3. Saving the section hierarchy
        4. Recording validation status

        Args:
            source_file (str): Path to the original markdown file.
                Used for document identification and tracking.
            data (Dict[str, Any]): The converted data structure to save.
                Should be a validated JSON structure containing sections.

        Returns:
            int: The unique identifier (ID) of the saved document.
                This can be used for future retrievals.

        Raises:
            ValueError: If document insertion fails
            RuntimeError: If any part of the save operation fails

        Example:
            >>> coordinator = DatabaseOperationsCoordinator()
            >>> data = {"doc.md": [{"title": "Test", "level": 1}]}
            >>> doc_id = coordinator.save("doc.md", data)
            >>> print(isinstance(doc_id, int))
            True
        """
        # Insert document and get ID
        document_id = self.db_handler.insert_document(source_file)
        if not document_id:
            raise ValueError("Failed to insert document")

        # Insert JSON output
        print(f"Inserting JSON output for document ID: {document_id}")
        self.db_handler.insert_json_output(document_id, data)

        # Insert sections
        root_section = data[list(data.keys())[0]][0]
        print(f"Inserting section for document ID: {document_id}")
        self.db_handler.insert_section(document_id, None, root_section)

        # Insert validation result (always valid at this point)
        print(f"Inserting validation result for document ID: {document_id}")
        self.db_handler.insert_validation_result(document_id, True)

        return document_id

    def truncate_tables(self) -> None:
        """Clear all data from database tables.

        Removes all records from all tables while maintaining table
        structure. This is useful for testing or resetting the database
        to a clean state.

        Note:
            This operation is irreversible and should be used with caution.

        Example:
            >>> coordinator = DatabaseOperationsCoordinator()
            >>> coordinator.truncate_tables()
            >>> docs = coordinator.db_handler.get_all_documents()
            >>> print(len(docs))
            0
        """
        self.db_handler.truncate_tables()

    def get_document(self, document_id: int) -> Optional[Tuple[int, str]]:
        """Retrieve document information by ID.

        Fetches basic document information including its ID and file path.
        Returns None if no document is found with the given ID.

        Args:
            document_id (int): The unique identifier of the document.

        Returns:
            Optional[Tuple[int, str]]: A tuple containing:
                - int: Document ID
                - str: Original file path
                Or None if document not found.

        Example:
            >>> coordinator = DatabaseOperationsCoordinator()
            >>> doc = coordinator.get_document(1)
            >>> if doc:
            ...     print(f"Found document: {doc[1]}")
        """
        docs = self.db_handler.get_all_documents()
        return next((doc for doc in docs if doc[0] == document_id), None)

    def get_json_output(self, document_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve stored JSON output for a document.

        Fetches the complete JSON structure that was saved for a document,
        including all sections and their hierarchy.

        Args:
            document_id (int): The unique identifier of the document.

        Returns:
            Optional[Dict[str, Any]]: The stored JSON structure or None
                if no output exists for the document.

        Example:
            >>> coordinator = DatabaseOperationsCoordinator()
            >>> output = coordinator.get_json_output(1)
            >>> if output:
            ...     print("First section:", list(output.values())[0][0])
        """
        return self.db_handler.get_json_output(document_id)

    def get_sections(self, document_id: int) -> list:
        """Retrieve all sections for a document.

        Fetches the complete list of sections associated with a document,
        maintaining their hierarchical relationships.

        Args:
            document_id (int): The unique identifier of the document.

        Returns:
            list: List of section records, each containing ID, parent ID,
                title, content, and level information.

        Example:
            >>> coordinator = DatabaseOperationsCoordinator()
            >>> sections = coordinator.get_sections(1)
            >>> print(f"Found {len(sections)} sections")
        """
        return self.db_handler.get_sections(document_id)

    def get_validation_result(self, document_id: int) -> Optional[Tuple[int, bool, str]]:
        """Retrieve validation result for a document.

        Fetches the stored validation status and any error messages
        associated with the document's validation.

        Args:
            document_id (int): The unique identifier of the document.

        Returns:
            Optional[Tuple[int, bool, str]]: A tuple containing:
                - int: Document ID
                - bool: Validation status (True if valid)
                - str: Error message (empty if valid)
                Or None if no validation result exists.

        Example:
            >>> coordinator = DatabaseOperationsCoordinator()
            >>> result = coordinator.get_validation_result(1)
            >>> if result:
            ...     print(f"Valid: {result[1]}")
        """
        return self.db_handler.get_validation_result(document_id)
