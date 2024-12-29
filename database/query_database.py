"""
Database query utility for inspecting conversion system data.

This module provides functionality to query and display the contents of
all tables in the markdown conversion database. It's useful for debugging,
data verification, and system monitoring.

Author:
    Tariq Ahmed (t.ahmed@stride.ae)

Organization:
    Stride Information Technology LLC

Features:
    - Environment variable configuration
    - Automated table content display
    - Connection management
    - Error handling
    - Formatted output

Example:
    To view database contents:
        $ python database/query_database.py

    This will display the contents of:
    - DOCUMENT table
    - SECTION table
    - JSON_OUTPUT table
    - VALIDATION_RESULT table
"""

import os
import psycopg2
from dotenv import load_dotenv
from typing import Dict, Any, List, Tuple

# SQL queries for each table
QUERIES: Dict[str, str] = {
    "DOCUMENT": "SELECT * FROM DOCUMENT;",
    "SECTION": "SELECT * FROM SECTION;",
    "JSON_OUTPUT": "SELECT * FROM JSON_OUTPUT;",
    "VALIDATION_RESULT": "SELECT * FROM VALIDATION_RESULT;"
}

def get_connection() -> psycopg2.extensions.connection:
    """Create a database connection using environment variables.

    Returns:
        psycopg2.extensions.connection: Active database connection

    Raises:
        psycopg2.Error: If connection fails
    """
    load_dotenv(dotenv_path='.env')
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )

def query_tables() -> None:
    """Query and display the contents of all database tables.

    Executes SELECT queries on all tables in the system and prints
    the results in a formatted manner. Handles connection lifecycle
    and ensures proper cleanup.

    Example:
        >>> query_tables()
        Querying database...
        
        Data from DOCUMENT table:
        (1, 'example.md')
        ...
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        print("Querying database...")
        
        for table, query in QUERIES.items():
            print(f"\nExecuting query for {table} table...")
            print(f"\nData from {table} table:")
            cur.execute(query)
            rows = cur.fetchall()
            for row in rows:
                print(row)
                
    except Exception as e:
        print(f"Failed to query database: {e}")
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    query_tables()
