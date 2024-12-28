# Project README

## Testing Before Integration
Thoroughly test the script before integrating it into your backend framework (e.g., FastAPI, Flask, Django, etc.).

## Adjustments for ORM Integration
Modify the script to ensure compatibility with your ORM (e.g., SQLAlchemy, Django ORM, or any other ORM in use).

## Script Purpose
The script serves the following purposes:

### Markdown to JSON Conversion
- Converts Markdown (`.md`) files into JSON format.
- Imports the converted data into a PostgreSQL database to achieve the following:
  1. Retrieve stored data from the database and loop through it to allow an AI agent to efficiently divide tasks, enhancing overall efficiency and reliability.
  2. Upcoming Feature: Update the script to support embedding files into a vector database, accommodating a more dynamic range of file types (e.g., PDF, XML, HTML, DOCX, Excel, CSV, etc.).

## Mermaid Diagrams

### Database Schema
The database schema includes the following tables:
- `DOCUMENT`: Stores document metadata such as filename, creation timestamp, and update timestamp.
- `SECTION`: Stores sections of the document, including title, content, level, position, and hierarchical path.
- `JSON_OUTPUT`: Stores the JSON content of the document.
- `VALIDATION_RESULT`: Stores the validation results of the document.

The relationships between the tables are as follows:
- A `DOCUMENT` can have many `SECTION` entries.
- A `SECTION` can have many child `SECTION` entries.
- A `DOCUMENT` can have many `JSON_OUTPUT` entries.
- A `DOCUMENT` can have one `VALIDATION_RESULT` entry.

```mermaid
erDiagram
    DOCUMENT {
        int id PK
        varchar filename
        timestamp created_at
        timestamp updated_at
    }
    SECTION {
        int id PK
        int document_id FK
        int parent_id FK
        varchar title
        text content
        int level
        int position
        ltree path
    }
    JSON_OUTPUT {
        int id PK
        int document_id FK
        text json_content
        timestamp created_at
    }
    VALIDATION_RESULT {
        int id PK
        int document_id FK
        boolean is_valid
        text errors
        timestamp validated_at
    }

    DOCUMENT ||--o{ SECTION : "has many"
    SECTION ||--o{ SECTION : "has many"
    DOCUMENT ||--o{ JSON_OUTPUT : "has many"
    DOCUMENT ||--o| VALIDATION_RESULT : "has one"
```
```

### Sequence Diagram
The sequence diagram illustrates the flow of data and interactions between the components of the script.

```mermaid
sequenceDiagram
    participant User
    participant Script
    participant Database
    User->>Script: Run convert_md_to_json.py
    Script->>Database: Connect to database
    Script->>Script: Read markdown file
    Script->>Script: Convert markdown to JSON
    Script->>Database: Insert document metadata
    Script->>Database: Insert JSON content
    Script->>Database: Insert sections
    Script->>Database: Insert validation results
    Script->>User: Output JSON file and validation results
```

### Class Diagram
The class diagram includes the following classes:
- `FileReader`: Reads the content of a file.
- `JSONWriter`: Writes JSON content to a file.
- `Validator`: Validates JSON content against a schema.
- `MarkdownConverter`: Converts markdown files to JSON and optionally saves the output to a database.

The relationships between the classes are as follows:
- `MarkdownConverter` uses `FileReader` to read the content of the markdown file.
- `MarkdownConverter` uses `JSONWriter` to write the JSON content to a file.
- `MarkdownConverter` uses `Validator` to validate the JSON content.

```mermaid
classDiagram
    class FileReader {
        +__init__(source_file: str)
        +read() List[str]
    }
    class JSONWriter {
        +__init__(output_path: str)
        +write(data: dict)
    }
    class Validator {
        +__init__()
        +validate(data: dict) -> Tuple[bool, str]
    }
    class MarkdownConverter {
        +__init__(source_file: str, output_path: Optional[str] = None, save_to_db: bool = False)
        +convert() -> str
        +_default_output_path() -> str
        +_establish_db_connection()
        +_insert_document() -> int
        +_insert_json_output(document_id: int, data: dict)
        +_insert_section(document_id: int, parent_id: Optional[int], section: dict)
        +_insert_validation_result(document_id: int, is_valid: bool, errors: str)
        +_save_to_database(data: dict)
        +_parse_markdown(content: List[str]) -> dict
    }
    FileReader --> MarkdownConverter
    JSONWriter --> MarkdownConverter
    Validator --> MarkdownConverter
```

## Contact
Feel free to contact me to achieve group and new ideas.
