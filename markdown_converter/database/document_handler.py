"""
Document handler module for document record management.

This module provides specialized functionality for managing document records
in the database, including creation, retrieval, and duplicate handling. It
ensures proper tracking of markdown documents in the system.

Author:
    Tariq Ahmed (t.ahmed@stride.ae)

Organization:
    Stride Information Technology LLC

Example:
    >>> handler = DocumentHandler()
    >>> try:
    ...     doc_id = handler.insert_document("example.md")
    ...     docs = handler.get_all_documents()
    ...     print(f"Found {len(docs)} documents")
    ... finally:
    ...     handler.close()
"""

from typing import List, Tuple, Dict, Any
from .base_handler import BaseHandler, DatabaseError

class DocumentHandler(BaseHandler):
    """Handles document record management in the database.

    This handler manages the DOCUMENT table in the database, providing
    operations for document creation and retrieval. It includes logic
    for handling duplicate documents and maintaining document metadata.

    The handler ensures:
    1. Unique document tracking by filename
    2. Proper document ID generation
    3. Efficient document retrieval
    4. Duplicate document handling

    Attributes:
        Inherits connection management from BaseHandler
    """

    def get_all_documents(self) -> List[Tuple[int, str]]:
        """Retrieve all document records from the database.

        Fetches a list of all documents currently tracked in the system,
        including their unique identifiers and filenames.

        Returns:
            List[Tuple[int, str]]: List of document records where each
                tuple contains:
                - int: Document ID
                - str: Original filename/path

        Example:
            >>> handler = DocumentHandler()
            >>> documents = handler.get_all_documents()
            >>> for doc_id, filename in documents:
            ...     print(f"Document {doc_id}: {filename}")
        """
        return self._execute_query("SELECT id, filename FROM DOCUMENT") or []

    def insert_document(self, file_path: str) -> int:
        """Create a new document record or retrieve existing one.

        Attempts to create a new document record in the database. If a
        document with the same filename already exists, returns the
        existing document's ID instead of creating a duplicate.

        Args:
            file_path (str): Path to the document file. Used as a unique
                identifier for the document.

        Returns:
            int: The document ID, either newly created or existing.

        Raises:
            DatabaseError: If document insertion fails or existing
                document cannot be retrieved.

        Example:
            >>> handler = DocumentHandler()
            >>> try:
            ...     doc_id = handler.insert_document("new_doc.md")
            ...     print(f"Document ID: {doc_id}")
            ... except DatabaseError as e:
            ...     print(f"Failed to insert: {e}")
        """
        try:
            result = self._execute_query(
                "INSERT INTO DOCUMENT (filename) VALUES (%s) RETURNING id",
                (file_path,)
            )
            if not result:
                raise DatabaseError("Failed to insert document")
            document_id = result[0]
            print(f"Inserted document with ID: {document_id}")
            return document_id
        except DatabaseError as e:
            if "duplicate key" in str(e).lower():
                result = self._execute_query(
                    "SELECT id FROM DOCUMENT WHERE filename = %s",
                    (file_path,)
                )
                if not result:
                    raise DatabaseError("Failed to find existing document")
                document_id = result[0][0]
                print(f"Document already exists with ID: {document_id}")
                return document_id
            raise
