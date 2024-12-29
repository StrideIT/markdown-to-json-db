"""
Output handler module for JSON data and validation results.

This module provides specialized functionality for managing the storage and
retrieval of JSON conversion outputs and their associated validation results.
It handles both initial storage and updates while maintaining data integrity.

Author:
    Tariq Ahmed (t.ahmed@stride.ae)

Organization:
    Stride Information Technology LLC

Example:
    >>> handler = OutputHandler()
    >>> try:
    ...     handler.insert_json_output(1, {"data": "content"})
    ...     handler.insert_validation_result(1, True)
    ...     result = handler.get_json_output(1)
    ...     print("Valid output stored" if result else "No output found")
    ... finally:
    ...     handler.close()
"""

from typing import Dict, Any, Optional, Tuple
import json
from .base_handler import BaseHandler, DatabaseError

class OutputHandler(BaseHandler):
    """Handles storage and retrieval of conversion outputs and results.

    This handler manages two key aspects of the conversion process:
    1. JSON output storage and retrieval
    2. Validation result tracking

    It provides atomic operations for storing and updating both types of
    data while maintaining referential integrity with document records.
    The handler includes logic for handling both new insertions and
    updates to existing records.

    Attributes:
        Inherits connection management from BaseHandler
    """

    def get_json_output(self, document_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve stored JSON output for a specific document.

        Fetches the JSON conversion output associated with a document,
        deserializing it from the database storage format into a Python
        dictionary.

        Args:
            document_id (int): Unique identifier of the document whose
                output should be retrieved.

        Returns:
            Optional[Dict[str, Any]]: The stored JSON data if found,
                deserialized into a Python dictionary. None if no output
                exists for the document.

        Example:
            >>> handler = OutputHandler()
            >>> output = handler.get_json_output(1)
            >>> if output:
            ...     print(f"Found output with {len(output)} keys")
        """
        result = self._execute_query(
            "SELECT json_content FROM JSON_OUTPUT WHERE document_id = %s",
            (document_id,)
        )
        if result and result[0] and result[0][0]:
            return json.loads(result[0][0])
        return None

    def insert_json_output(self, document_id: int, json_data: Dict[str, Any]) -> None:
        """Store or update JSON output for a document.

        Attempts to store new JSON output for a document. If output already
        exists for the document, updates it instead. The JSON data is
        serialized before storage.

        Args:
            document_id (int): Unique identifier of the document this
                output belongs to.
            json_data (Dict[str, Any]): The JSON data to store. Must be
                JSON-serializable.

        Raises:
            DatabaseError: If the storage operation fails or if the data
                cannot be serialized.

        Example:
            >>> handler = OutputHandler()
            >>> try:
            ...     handler.insert_json_output(1, {
            ...         "sections": [{"title": "Test"}]
            ...     })
            ... except DatabaseError as e:
            ...     print(f"Storage failed: {e}")
        """
        try:
            self._execute_query(
                "INSERT INTO JSON_OUTPUT (document_id, json_content) VALUES (%s, %s)",
                (document_id, json.dumps(json_data))
            )
            print(f"Inserted JSON output for document ID: {document_id}")
        except DatabaseError as e:
            if "duplicate key" in str(e).lower():
                self._execute_query(
                    "UPDATE JSON_OUTPUT SET json_content = %s WHERE document_id = %s",
                    (json.dumps(json_data), document_id)
                )
                print(f"Updated JSON output for document ID: {document_id}")
            else:
                raise

    def get_validation_result(self, document_id: int) -> Optional[Tuple[int, bool, str]]:
        """Retrieve validation result for a specific document.

        Fetches the stored validation result for a document, including
        its validation status and any error messages from failed
        validations.

        Args:
            document_id (int): Unique identifier of the document whose
                validation result should be retrieved.

        Returns:
            Optional[Tuple[int, bool, str]]: If found, a tuple containing:
                - int: Result ID
                - bool: Validation status (True if valid)
                - str: Error messages (empty if valid)
                None if no validation result exists.

        Example:
            >>> handler = OutputHandler()
            >>> result = handler.get_validation_result(1)
            >>> if result:
            ...     _, is_valid, errors = result
            ...     print("Valid" if is_valid else f"Invalid: {errors}")
        """
        result = self._execute_query("""
            SELECT id, is_valid, errors 
            FROM VALIDATION_RESULT 
            WHERE document_id = %s
        """, (document_id,))
        return result[0] if result else None

    def insert_validation_result(self, document_id: int, is_valid: bool, errors: str = '') -> None:
        """Store or update validation result for a document.

        Records the validation status and any error messages for a
        document. If a validation result already exists for the document,
        updates it instead of creating a new record.

        Args:
            document_id (int): Unique identifier of the document this
                validation result belongs to.
            is_valid (bool): Whether the document passed validation.
            errors (str, optional): Error messages if validation failed.
                Should be empty if is_valid is True. Defaults to ''.

        Raises:
            DatabaseError: If the storage operation fails or if the
                document doesn't exist.

        Example:
            >>> handler = OutputHandler()
            >>> try:
            ...     handler.insert_validation_result(
            ...         1, False, "Missing required fields"
            ...     )
            ... except DatabaseError as e:
            ...     print(f"Failed to store result: {e}")
        """
        try:
            self._execute_query("""
                INSERT INTO VALIDATION_RESULT (document_id, is_valid, errors)
                VALUES (%s, %s, %s)
            """, (document_id, is_valid, errors))
            print(f"Inserted validation result for document ID: {document_id}")
        except DatabaseError as e:
            if "duplicate key" in str(e).lower():
                self._execute_query("""
                    UPDATE VALIDATION_RESULT 
                    SET is_valid = %s, errors = %s 
                    WHERE document_id = %s
                """, (is_valid, errors, document_id))
                print(f"Updated validation result for document ID: {document_id}")
            else:
                raise
