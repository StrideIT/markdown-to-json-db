"""
Base database handler module for common database operations.

This module provides the foundational database handling functionality used
across all database operations. It implements connection management,
transaction control, and error handling while supporting configuration
through environment variables.

Author:
    Tariq Ahmed (t.ahmed@stride.ae)

Organization:
    Stride Information Technology LLC

Example:
    >>> class CustomHandler(BaseHandler):
    ...     def get_record(self, id: int):
    ...         return self._execute_query(
    ...             "SELECT * FROM records WHERE id = %s",
    ...             (id,)
    ...         )
    >>> handler = CustomHandler()
    >>> try:
    ...     handler._execute_query("SELECT 1")
    ...     handler.commit()
    ... finally:
    ...     handler.close()
"""

import psycopg2
from typing import Optional, Any
import os

class DatabaseError(Exception):
    """Custom exception class for database-specific errors.

    This exception is raised when database operations fail, providing
    a clean way to distinguish database errors from other types of
    errors in the application.

    Attributes:
        message (str): Detailed error message explaining the database error
    """
    pass

class BaseHandler:
    """Base class providing common database functionality.

    This class implements core database operations and connection management
    that are shared across all database handlers. It handles connection
    setup, query execution, transaction management, and cleanup.

    The handler uses environment variables for configuration:
    - DB_HOST: Database server host (default: localhost)
    - DB_PORT: Database server port (default: 5433)
    - DB_NAME: Database name (default: mcp)
    - DB_USER: Database user (default: postgres)
    - DB_PASSWORD: Database password (default: stride)

    Attributes:
        conn (psycopg2.extensions.connection): Database connection object
    """

    def __init__(self):
        """Initialize database connection."""
        self.conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5433'),
            database=os.getenv('DB_NAME', 'mcp'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', 'stride')
        )
        self.conn.autocommit = False

    def _execute_query(self, query: str, params: Optional[tuple] = None) -> Any:
        """Execute a database query with proper error handling.

        Executes the provided SQL query with optional parameters, handling
        different query types (SELECT, INSERT, etc.) appropriately. Manages
        transactions and provides proper error handling and rollback.

        Args:
            query (str): SQL query to execute. Can be any valid SQL statement.
            params (Optional[tuple], optional): Query parameters for
                parameterized queries. Defaults to None.

        Returns:
            Any: Query results depending on the query type:
                - SELECT: List of result rows
                - INSERT/UPDATE with RETURNING: Single row
                - Other statements: None

        Raises:
            DatabaseError: If query execution fails for any reason
                (connection issues, SQL errors, etc.)

        Example:
            >>> handler = BaseHandler()
            >>> try:
            ...     result = handler._execute_query(
            ...         "SELECT * FROM table WHERE id = %s",
            ...         (42,)
            ...     )
            ... except DatabaseError as e:
            ...     print(f"Query failed: {e}")
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, params)
                if query.strip().upper().startswith('SELECT'):
                    return cursor.fetchall()
                elif 'RETURNING' in query.upper():
                    return cursor.fetchone()
                self.conn.commit()
        except psycopg2.Error as e:
            self.conn.rollback()
            raise DatabaseError(f"Database error: {str(e)}")

    def commit(self) -> None:
        """Commit the current database transaction.

        Commits any pending changes in the current transaction to the
        database, making them permanent. Should be called after successful
        operations that modify data.

        Raises:
            DatabaseError: If commit fails

        Example:
            >>> handler = BaseHandler()
            >>> try:
            ...     handler._execute_query("INSERT INTO ...")
            ...     handler.commit()
            ... except DatabaseError:
            ...     handler.rollback()
        """
        self.conn.commit()

    def rollback(self) -> None:
        """Rollback the current database transaction.

        Reverts any pending changes in the current transaction,
        returning the database to its state before the transaction
        began. Used for error recovery.

        Example:
            >>> handler = BaseHandler()
            >>> try:
            ...     handler._execute_query("UPDATE ...")
            ... except DatabaseError:
            ...     handler.rollback()
            ...     print("Transaction rolled back")
        """
        self.conn.rollback()

    def close(self) -> None:
        """Close the database connection and release resources.

        Properly closes the database connection, ensuring all resources
        are released. Should be called when the handler is no longer
        needed.

        Example:
            >>> handler = BaseHandler()
            >>> try:
            ...     handler._execute_query("SELECT 1")
            ... finally:
            ...     handler.close()
        """
        self.conn.close()
