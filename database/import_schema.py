import os
import psycopg2

"""
Author: Tariq Ahmed
Email: t.ahmed@stride.ae
Organization: Stride Information Technology

This module provides the import_schema function for importing the database schema from a SQL file.
"""

def import_schema():
    """
    Import the database schema from a SQL file.

    This function reads the schema SQL file and executes it to create the necessary database tables and indexes.
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
