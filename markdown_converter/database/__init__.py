"""
Database package for persistent storage of markdown conversion data.

This package provides a comprehensive database management system for storing
and retrieving markdown conversion results. It implements a modular architecture
with specialized handlers for different aspects of data management.

Author:
    Tariq Ahmed (t.ahmed@stride.ae)

Organization:
    Stride Information Technology LLC

Components:
    - Document Management: Handles document metadata and relationships
    - Section Management: Manages hierarchical content structure
    - Output Management: Stores JSON conversion results
    - Validation Management: Tracks data validation status

Features:
    - ACID compliant transactions
    - Hierarchical data storage
    - Automatic connection management
    - Error handling and recovery
    - Transaction isolation

Example:
    >>> from markdown_converter.database import DatabaseHandler
    >>> db = DatabaseHandler()
    >>> try:
    ...     doc_id = db.insert_document('example.md')
    ...     db.insert_json_output(doc_id, {"content": "..."})
    ...     db.commit()
    ... except DatabaseError as e:
    ...     db.rollback()
    ...     print(f"Database error: {e}")
    ... finally:
    ...     db.close()
"""

from typing import List, Dict, Any, Tuple, Optional
from .base_handler import BaseHandler, DatabaseError
from .document_handler import DocumentHandler
from .section_handler import SectionHandler
from .output_handler import OutputHandler

class DatabaseHandler:
    """Main database handler coordinating all database operations.

    This class serves as the central point for all database interactions,
    coordinating multiple specialized handlers through a unified interface.
    It manages the complete lifecycle of database operations including
    connection management, transaction control, and error handling.

    The handler uses a modular architecture where each type of operation
    (documents, sections, outputs) is managed by a dedicated handler class.
    This design allows for better separation of concerns and easier
    maintenance.

    Attributes:
        document_handler (DocumentHandler): Manages document-related operations
        section_handler (SectionHandler): Handles section data and hierarchy
        output_handler (OutputHandler): Manages JSON output and validation results

    Note:
        All operations are transactional and follow ACID principles. Use
        commit() to persist changes or rollback() to undo them.
    """

    def __init__(self):
        """Initialize database handlers."""
        self.document_handler = DocumentHandler()
        self.section_handler = SectionHandler()
        self.output_handler = OutputHandler()

    def truncate_tables(self) -> None:
        """Truncate all tables in the database."""
        self.document_handler._execute_query("""
            TRUNCATE TABLE VALIDATION_RESULT CASCADE;
            TRUNCATE TABLE SECTION CASCADE;
            TRUNCATE TABLE JSON_OUTPUT CASCADE;
            TRUNCATE TABLE DOCUMENT CASCADE;
        """)
        print("All tables truncated successfully.")

    # Document operations
    def get_all_documents(self) -> List[Tuple[int, str]]:
        """Get all documents from the database."""
        return self.document_handler.get_all_documents()

    def insert_document(self, file_path: str) -> int:
        """Insert a new document record."""
        document_id = self.document_handler.insert_document(file_path)
        self.document_handler.commit()  # Commit immediately to make ID available
        return document_id

    # Section operations
    def get_sections(self, document_id: int) -> List[Tuple[int, Optional[int], str, str, int]]:
        """Get all sections for a document."""
        return self.section_handler.get_sections(document_id)

    def insert_section(self, document_id: int, parent_id: Optional[int], section_data: Dict[str, Any]) -> int:
        """Insert a section record."""
        # Debug print
        print(f"DatabaseHandler insert_section: {section_data}")
        
        # Ensure content is properly handled
        if 'content' not in section_data:
            section_data['content'] = ''
        elif section_data['content'] is None:
            section_data['content'] = ''
            
        section_id = self.section_handler.insert_section(document_id, parent_id, section_data)
        self.section_handler.commit()  # Commit immediately to maintain consistency
        return section_id

    # JSON output operations
    def get_json_output(self, document_id: int) -> Optional[Dict[str, Any]]:
        """Get JSON output for a document."""
        return self.output_handler.get_json_output(document_id)

    def insert_json_output(self, document_id: int, json_data: Dict[str, Any]) -> None:
        """Insert JSON output for a document."""
        self.output_handler.insert_json_output(document_id, json_data)
        self.output_handler.commit()  # Commit immediately to maintain consistency

    # Validation result operations
    def get_validation_result(self, document_id: int) -> Optional[Tuple[int, bool, str]]:
        """Get validation result for a document."""
        return self.output_handler.get_validation_result(document_id)

    def insert_validation_result(self, document_id: int, is_valid: bool, errors: str = '') -> None:
        """Insert validation result for a document."""
        self.output_handler.insert_validation_result(document_id, is_valid, errors)
        self.output_handler.commit()  # Commit immediately to maintain consistency

    def commit(self) -> None:
        """Commit transactions in all handlers."""
        self.document_handler.commit()
        self.section_handler.commit()
        self.output_handler.commit()

    def rollback(self) -> None:
        """Rollback transactions in all handlers."""
        self.document_handler.rollback()
        self.section_handler.rollback()
        self.output_handler.rollback()

    def close(self) -> None:
        """Close all database connections."""
        self.document_handler.close()
        self.section_handler.close()
        self.output_handler.close()

# Export classes for easy access
__all__ = ['DatabaseHandler', 'DatabaseError']
