import re
import os
import psycopg2
import json
from typing import Optional, List, Dict, Any, Union
from psycopg2.extensions import connection
from .file_reader import FileReader
from .json_writer import JSONWriter
from .validator import Validator

"""
Author: Tariq Ahmed
Email: t.ahmed@stride.ae
Organization: Stride Information Technology

This module provides the MarkdownConverter class for converting markdown files to JSON and optionally saving the output to a database.
"""

class MarkdownConverter:
    def __init__(self, source_file: str, output_path: Optional[str] = None, save_to_db: bool = False):
        """
        Initialize the MarkdownConverter.

        Args:
            source_file (str): The path to the source markdown file.
            output_path (Optional[str]): The path to save the converted output. Defaults to None.
            save_to_db (bool): Flag to determine if the output should be saved to the database. Defaults to False.
        """
        self.source_file = source_file
        self.output_path = output_path or self._default_output_path()
        self.save_to_db = save_to_db
        self.file_reader = FileReader(source_file)
        self.json_writer = JSONWriter(self.output_path)
        self.validator = Validator()
        self.db_conn: Optional[connection] = None
        if self.save_to_db:
            self._establish_db_connection()

    def _default_output_path(self) -> str:
        """
        Generate the default output path for the converted JSON file.

        Returns:
            str: The default output path.
        """
        source_dir = os.path.dirname(self.source_file)
        source_filename = os.path.splitext(os.path.basename(self.source_file))[0]
        return os.path.join(source_dir, f"{source_filename}.json")

    def _establish_db_connection(self):
        """
        Establish a database connection.
        """
        db_host = os.getenv('DB_HOST')
        db_port = os.getenv('DB_PORT')
        db_name = os.getenv('DB_NAME')
        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')

        self.db_conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password
        )

    def convert(self) -> str:
        """
        Convert the markdown file to JSON and optionally save the output to a database.

        Returns:
            str: The path to the converted JSON file.
        """
        content = self.file_reader.read()
        data = self._parse_markdown(content)
        self.json_writer.write(data)
        self.validator.validate(data)
        if self.save_to_db:
            self._save_to_database(data)
        return self.output_path

    def _insert_document(self) -> int:
        """
        Insert a document into the DOCUMENT table and return the document ID.

        Returns:
            int: The document ID.

        Raises:
            ValueError: If the database connection is not established or if the document ID retrieval fails.
        """
        if self.db_conn is None:
            raise ValueError("Database connection is not established.")
        cur = self.db_conn.cursor()
        cur.execute(
            "INSERT INTO DOCUMENT (filename, created_at, updated_at) VALUES (%s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP) RETURNING id",
            (self.source_file,)
        )
        result = cur.fetchone()
        if result is None:
            raise ValueError("Failed to retrieve document ID.")
        document_id = result[0]
        self.db_conn.commit()
        cur.close()
        return document_id

    def _insert_json_output(self, document_id: int, data: dict):
        """
        Insert JSON output into the JSON_OUTPUT table.

        Args:
            document_id (int): The document ID.
            data (dict): The JSON data to be inserted.

        Raises:
            ValueError: If the database connection is not established.
        """
        if self.db_conn is None:
            raise ValueError("Database connection is not established.")
        cur = self.db_conn.cursor()
        cur.execute(
            "INSERT INTO JSON_OUTPUT (document_id, json_content, created_at) VALUES (%s, %s, CURRENT_TIMESTAMP)",
            (document_id, json.dumps(data))
        )
        self.db_conn.commit()
        cur.close()

    def _insert_section(self, document_id, parent_id, section):
        """
        Insert a section into the SECTION table.

        Args:
            document_id: The document ID.
            parent_id: The parent section ID.
            section: The section data to be inserted.

        Raises:
            KeyError: If the section does not contain 'title' and 'content' keys.
            ValueError: If the database connection is not established.
        """
        if 'title' not in section or 'content' not in section:
            raise KeyError("Section must contain 'title' and 'content' keys")
        
        if self.db_conn is None:
            raise ValueError("Database connection is not established.")
        cur = self.db_conn.cursor()
        cur.execute(
            """
            INSERT INTO SECTION (document_id, parent_id, title, content, level, position, path)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (document_id, parent_id, section['title'], section['content'], section['level'], section.get('position', 0), section.get('path', ''))
        )
        result = cur.fetchone()
        if result is None:
            raise ValueError("Failed to retrieve section ID.")
        section_id = result[0]
        if section.get('children'):
            for child in section['children']:
                self._insert_section(document_id, section_id, child)

    def _insert_validation_result(self, document_id: int, is_valid: bool, errors: str):
        """
        Insert validation result into the VALIDATION_RESULT table.

        Args:
            document_id (int): The document ID.
            is_valid (bool): The validation result.
            errors (str): The validation errors.

        Raises:
            ValueError: If the database connection is not established.
        """
        if self.db_conn is None:
            raise ValueError("Database connection is not established.")
        cur = self.db_conn.cursor()
        cur.execute(
            "INSERT INTO VALIDATION_RESULT (document_id, is_valid, errors, validated_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP)",
            (document_id, is_valid, errors)
        )
        self.db_conn.commit()
        cur.close()

    def _save_to_database(self, data: dict):
        """
        Save the converted data to the database.

        Args:
            data (dict): The converted JSON data.

        Raises:
            ValueError: If the database connection is not established.
        """
        if self.db_conn is None:
            raise ValueError("Database connection is not established.")
        document_id = self._insert_document()
        self._insert_json_output(document_id, data)
        root_section = data[list(data.keys())[0]][0]
        self._insert_section(document_id, None, root_section)
        is_valid, errors = self.validator.validate(data)
        self._insert_validation_result(document_id, is_valid, errors)

    def _parse_markdown(self, content: List[str]) -> dict:
        """
        Parse the markdown content and convert it to a JSON structure.

        Args:
            content (List[str]): The markdown content to be parsed.

        Returns:
            dict: The parsed JSON structure.
        """
        stack: List[Dict[str, Any]] = []
        current_content: List[str] = []
        root: List[Dict[str, Any]] = []
        first_level_1: Optional[Dict[str, Any]] = None

        for line in content:
            line = line.strip()
            if not line:
                continue

            heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if heading_match:
                if current_content and stack:
                    stack[-1]["content"] = "\n".join(current_content)
                current_content = []

                level = len(heading_match.group(1))
                title = heading_match.group(2)

                new_node = {
                    "title": title,
                    "content": "",
                    "level": level,
                    "children": []
                }

                if level == 1:
                    if first_level_1 is None:
                        first_level_1 = new_node
                        root.append(first_level_1)
                        stack = [new_node]
                    else:
                        first_level_1["children"].append(new_node)
                        stack = [new_node]
                    continue

                while stack and stack[-1]["level"] >= level:
                    stack.pop()

                if stack:
                    parent = stack[-1]
                    parent["children"].append(new_node)
                else:
                    root.append(new_node)

                stack.append(new_node)
            else:
                current_content.append(line)

        if current_content and stack:
            stack[-1]["content"] = "\n".join(current_content)

        # Return the parsed JSON structure with the document title and content.
        return {
            os.path.basename(self.source_file): [
                {
                    "title": first_level_1["title"] if first_level_1 else "Document",
                    "content": first_level_1["content"] if first_level_1 else "",
                    "level": 1,
                    "children": root
                }
            ]
        }
