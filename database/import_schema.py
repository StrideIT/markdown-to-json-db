import os
import psycopg2

"""
Database schema import module for markdown conversion system.

This module provides functionality to import and initialize the database
schema required for the markdown conversion system. It reads the schema
definition from a SQL file and executes it to create the necessary
database structure.

Author:
    Tariq Ahmed (t.ahmed@stride.ae)

Organization:
    Stride Information Technology LLC

Features:
    - Environment variable configuration
    - Automated schema import
    - SQL file parsing
    - Connection management
    - Error handling

Example:
    To import the schema:
        $ python database/import_schema.py

    This will:
    1. Connect to the configured database
    2. Read the schema from database_schema.sql
    3. Execute the schema creation commands
"""

def import_schema() -> None:
    """Import and initialize the database schema.

    Reads the database schema definition from the SQL file and executes
    it to create or update the database structure. This includes:
    - Creating tables
    - Setting up indexes
    - Defining constraints
    - Establishing relationships

    The function uses environment variables for database configuration:
    - DB_HOST: Database server host
    - DB_PORT: Database server port
    - DB_NAME: Target database name
    - DB_USER: Database user
    - DB_PASSWORD: Database password

    Raises:
        psycopg2.Error: If database connection or execution fails
        FileNotFoundError: If schema file cannot be found or read

    Example:
        >>> import_schema()
        # Database schema will be imported...
        # Tables and indexes will be created...
    """
    # Get database connection details from environment variables
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')

    # Connect to the database
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        dbname=db_name,
        user=db_user,
        password=db_password
    )
    cursor = conn.cursor()

    # Read the schema file
    with open(os.path.join(os.path.dirname(__file__), 'database_schema.sql'), 'r') as f:
        schema_sql = f.read()

    # Execute the schema SQL
    cursor.execute(schema_sql)
    conn.commit()

    # Close the connection
    cursor.close()
    conn.close()

if __name__ == '__main__':
    import_schema()
