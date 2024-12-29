"""
Database truncation utility for clearing all tables.

This module provides functionality to truncate all tables in the database
while maintaining the schema structure. It's useful for clearing test data
and resetting the system to a clean state.

Author:
    Tariq Ahmed (t.ahmed@stride.ae)

Organization:
    Stride Information Technology LLC

Features:
    - Complete data removal
    - Identity sequence reset
    - Cascading truncation
    - Environment variable configuration
    - Connection management
    - Error handling

Example:
    To truncate all tables:
        $ python database/truncate_tables.py

    This will:
    1. Clear all data from all tables
    2. Reset all identity sequences
    3. Maintain table structure and relationships
"""

import os
import psycopg2
from dotenv import load_dotenv
from typing import Optional

# Default database configuration
DEFAULT_CONFIG = {
    'DB_HOST': 'localhost',
    'DB_PORT': '5433',
    'DB_NAME': 'mcp',
    'DB_USER': 'postgres',
    'DB_PASSWORD': 'stride'
}

# SQL command to truncate all tables
TRUNCATE_SQL = """
TRUNCATE TABLE validation_result RESTART IDENTITY CASCADE;
TRUNCATE TABLE json_output RESTART IDENTITY CASCADE;
TRUNCATE TABLE section RESTART IDENTITY CASCADE;
TRUNCATE TABLE document RESTART IDENTITY CASCADE;
"""

def setup_environment() -> None:
    """Configure database environment variables.

    Sets up the database connection configuration using either
    environment variables or default values.
    """
    for key, value in DEFAULT_CONFIG.items():
        if not os.getenv(key):
            os.environ[key] = value

def get_connection() -> psycopg2.extensions.connection:
    """Create a database connection using environment variables.

    Returns:
        psycopg2.extensions.connection: Active database connection

    Raises:
        psycopg2.Error: If connection fails
    """
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )

def truncate_tables() -> None:
    """Truncate all tables in the database.

    Executes TRUNCATE commands on all tables with RESTART IDENTITY
    and CASCADE options to ensure complete data removal while
    maintaining referential integrity.

    Example:
        >>> truncate_tables()
        All tables truncated successfully.
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(TRUNCATE_SQL)
        conn.commit()
        print("All tables truncated successfully.")

    except Exception as e:
        print(f"Failed to truncate tables: {e}")
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    setup_environment()
    truncate_tables()
