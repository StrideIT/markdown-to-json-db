"""
Database recreation utility for resetting the database schema.

This module provides functionality to completely recreate the database
schema by executing the schema SQL script. It's useful for development,
testing, and system resets.

Author:
    Tariq Ahmed (t.ahmed@stride.ae)

Organization:
    Stride Information Technology LLC

Features:
    - Complete schema recreation
    - Environment variable configuration
    - SQL script execution
    - Connection management
    - Error handling

Example:
    To recreate the database schema:
        $ python database/recreate_tables.py

    This will:
    1. Drop all existing tables
    2. Create new tables with fresh schema
    3. Set up all constraints and indexes
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

def recreate_tables() -> None:
    """Recreate all database tables from schema.

    Reads the database schema SQL file and executes it to drop and
    recreate all tables. This provides a clean slate for the database.

    Example:
        >>> recreate_tables()
        Database tables recreated successfully.
    """
    conn = None
    cur = None
    try:
        # Read schema file
        with open('database/database_schema.sql', 'r') as file:
            sql_script = file.read()

        # Execute schema recreation
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(sql_script)
        conn.commit()
        print("Database tables recreated successfully.")

    except Exception as e:
        print(f"Failed to recreate database tables: {e}")
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    setup_environment()
    recreate_tables()
