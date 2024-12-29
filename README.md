# Markdown to JSON Database Converter

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PostgreSQL 13+](https://img.shields.io/badge/postgresql-13+-blue.svg)](https://www.postgresql.org/)

## Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Component Documentation](#component-documentation)
4. [Installation & Setup](#installation--setup)
5. [Usage Guide](#usage-guide)
6. [Development Guide](#development-guide)
7. [API Reference](#api-reference)
8. [Testing](#testing)
9. [Contributing](#contributing)
10. [License & Contact](#license--contact)

## Overview

A robust Python-based system designed to convert Markdown documents into structured JSON while persisting the data in a PostgreSQL database. The system maintains document hierarchy, supports nested sections, and ensures data integrity through comprehensive validation.

### Key Features
- Markdown to JSON conversion with hierarchy preservation
- Robust validation system with detailed error reporting
- PostgreSQL database integration with ACID compliance
- Support for nested document sections
- Comprehensive error handling and reporting

## System Architecture

### Use Case Overview

The following diagram illustrates the system's primary use cases and interactions:

```mermaid
flowchart TB
    %% Actors
    User(("👤 User"))
    System(("⚙️ System"))
    Database[("🗄️ Database")]

    %% System Boundary
    subgraph Markdown to JSON System
        %% Primary Use Cases
        Convert["📄 Convert Markdown to JSON"]
        Validate["✅ Validate Document"]
        SaveDB["💾 Save to Database"]
        
        %% Validation Use Cases
        subgraph Validation System
            direction TB
            ValidateSchema["🔍 Schema Validation"]
            ValidateContent["📝 Content Validation"]
            ValidateStructure["🌳 Structure Validation"]
            FormatErrors["❌ Error Formatting"]
        end

        %% Database Use Cases
        subgraph Database Operations
            direction TB
            SaveDoc["📋 Save Document"]
            SaveSections["📑 Save Sections"]
            SaveJSON["🔄 Save JSON"]
            SaveValidation["📊 Save Results"]
        end
    end

    %% Relationships
    User --> Convert
    Convert --> Validate
    Validate --> ValidateSchema
    Validate --> ValidateContent
    Validate --> ValidateStructure
    ValidateSchema --> FormatErrors
    ValidateContent --> FormatErrors
    ValidateStructure --> FormatErrors
    
    Convert --> SaveDB
    SaveDB --> SaveDoc
    SaveDB --> SaveSections
    SaveDB --> SaveJSON
    SaveDB --> SaveValidation
    
    SaveDoc --> Database
    SaveSections --> Database
    SaveJSON --> Database
    SaveValidation --> Database
    
    %% Add descriptions using native styling
    Convert -. "1. Reads markdown file<br/>2. Parses content<br/>3. Generates JSON" .-> System
    Validate -. "1. Schema validation<br/>2. Content validation<br/>3. Structure validation" .-> System
    SaveDB -. "1. Document metadata<br/>2. Section hierarchy<br/>3. JSON output<br/>4. Validation results" .-> System
```

### Component Architecture

The system is built using a modular architecture with clear separation of concerns:

```mermaid
classDiagram
    %% Core Components
    class FileReader {
        -source_file: str
        +__init__(source_file: str)
        +read() List[str]
    }

    class JSONWriter {
        -output_path: str
        +__init__(output_path: str)
        +write(data: dict)
    }

    class MarkdownParser {
        -source_file: str
        +__init__(source_file: str)
        +parse(content: List[str]) dict
    }

    class DatabaseHandler {
        -db_conn: Optional[connection]
        +__init__()
        -_establish_db_connection()
        +insert_document(source_file: str) int
        +insert_json_output(document_id: int, data: dict)
        +insert_section(document_id: int, parent_id: Optional[int], section: Dict[str, Any])
        +insert_validation_result(document_id: int, is_valid: bool, errors: str)
        +section_exists(document_id: int, title: str, content: str) bool
    }

    class MarkdownConverter {
        -source_file: str
        -output_path: Optional[str]
        -save_to_db: bool
        -file_reader: FileReader
        -json_writer: JSONWriter
        -validator: Validator
        -parser: MarkdownParser
        -db_handler: Optional[DatabaseHandler]
        +__init__(source_file: str, output_path: Optional[str], save_to_db: bool)
        +convert() str
        -_default_output_path() str
        -_save_to_database(data: dict)
    }

    %% Validation Components
    class ValidationStrategy {
        <<abstract>>
        #error_formatter: ErrorFormatter
        +__init__()
        +validate(data: Dict[str, Any])* Tuple[bool, Optional[ValidationError]]
        #_check_type(value: Any, expected_type: type, context: str) bool
        #_check_not_empty(value: Any, context: str) bool
    }

    class ErrorFormatter {
        +format_type_error(value: Any, expected_type: type, context: str) str
        +format_empty_error(context: str) str
        +format_structure_error(context: str, message: str) str
        +format_missing_field_error(fields: str, context: str) str
    }

    class ValidationError {
        -message: str
        +__init__(message: str)
        +__str__() str
    }

    class SchemaValidator {
        -required_fields: Set[str]
        +__init__()
        +validate(data: Dict[str, Any]) Tuple[bool, Optional[ValidationError]]
        -_validate_section(section: Dict[str, Any], context: str) Tuple[bool, Optional[ValidationError]]
    }

    class ContentValidator {
        +validate(data: Dict[str, Any]) Tuple[bool, Optional[ValidationError]]
        -_validate_section(section: Dict[str, Any], parent: str) Tuple[bool, Optional[ValidationError]]
    }

    class StructureValidator {
        +validate(data: Dict[str, Any]) Tuple[bool, Optional[ValidationError]]
        -_validate_children(section: Dict[str, Any], context: str, parent_level: int) Tuple[bool, Optional[ValidationError]]
    }

    class Validator {
        -schema_validator: SchemaValidator
        -content_validator: ContentValidator
        -structure_validator: StructureValidator
        +__init__()
        +validate(data: Dict[str, Any]) Tuple[bool, str]
    }

    %% Relationships
    MarkdownConverter --> FileReader : uses
    MarkdownConverter --> JSONWriter : uses
    MarkdownConverter --> Validator : uses
    MarkdownConverter --> MarkdownParser : uses
    MarkdownConverter --> DatabaseHandler : uses

    ValidationStrategy <|-- SchemaValidator : implements
    ValidationStrategy <|-- ContentValidator : implements
    ValidationStrategy <|-- StructureValidator : implements
    ValidationStrategy --> ErrorFormatter : uses
    ValidationStrategy --> ValidationError : creates

    Validator --> SchemaValidator : uses
    Validator --> ContentValidator : uses
    Validator --> StructureValidator : uses
```

### Database Schema

The system uses a PostgreSQL database with the following schema:

```mermaid
erDiagram
    %% Document Management
    DOCUMENT {
        bigserial id PK "Primary Key"
        varchar(255) filename "NOT NULL, Source markdown file"
        timestamp created_at "NOT NULL, DEFAULT CURRENT_TIMESTAMP"
        timestamp updated_at "NOT NULL, DEFAULT CURRENT_TIMESTAMP"
    }

    %% Section Hierarchy
    SECTION {
        bigserial id PK "Primary Key"
        bigint document_id FK "Foreign Key (DOCUMENT.id)"
        bigint parent_id FK "Foreign Key (SECTION.id), NULL for root sections"
        varchar(255) title "NOT NULL, Section heading"
        text content "NOT NULL, Section content"
        integer level "NOT NULL, Section heading level (1-6)"
        integer position "NOT NULL, DEFAULT 0, Order in document"
        ltree path "Hierarchical path in document structure"
    }

    %% JSON Representation
    JSON_OUTPUT {
        bigserial id PK "Primary Key"
        bigint document_id FK "Foreign Key (DOCUMENT.id)"
        jsonb json_content "NOT NULL, Converted document structure"
        timestamp created_at "NOT NULL, DEFAULT CURRENT_TIMESTAMP"
    }

    %% Validation Results
    VALIDATION_RESULT {
        bigserial id PK "Primary Key"
        bigint document_id FK "Foreign Key (DOCUMENT.id)"
        boolean is_valid "NOT NULL, Overall validation status"
        text errors "Validation errors from schema/content/structure validators"
        timestamp validated_at "NOT NULL, DEFAULT CURRENT_TIMESTAMP"
    }

    %% Relationships with cardinality and descriptions
    DOCUMENT ||--o{ SECTION : "contains sections in hierarchical structure"
    SECTION ||--o{ SECTION : "has child sections (recursive relationship)"
    DOCUMENT ||--o{ JSON_OUTPUT : "has JSON representation of document"
    DOCUMENT ||--o{ VALIDATION_RESULT : "has validation status and errors"
```

### Processing Flow

The sequence diagram below illustrates the system's processing flow:

```mermaid
sequenceDiagram
    autonumber
    participant User
    participant MC as MarkdownConverter
    participant FR as FileReader
    participant MP as MarkdownParser
    participant JW as JSONWriter
    participant V as Validator
    participant SV as SchemaValidator
    participant CV as ContentValidator
    participant StV as StructureValidator
    participant EF as ErrorFormatter
    participant DB as DatabaseHandler

    %% Initialize components
    User->>+MC: new MarkdownConverter(source_file, output_path, save_to_db)
    MC->>FR: new FileReader(source_file)
    MC->>JW: new JSONWriter(output_path)
    MC->>V: new Validator()
    Note over V: Creates validation components
    V->>SV: new SchemaValidator()
    V->>CV: new ContentValidator()
    V->>StV: new StructureValidator()
    Note over SV,StV: Each validator has ErrorFormatter
    MC->>MP: new MarkdownParser(source_file)
    alt save_to_db is true
        MC->>DB: new DatabaseHandler()
    end
    MC-->>-User: instance

    %% Convert markdown to JSON
    User->>+MC: convert()
    MC->>+FR: read()
    FR-->>-MC: content: List[str]
    
    MC->>+MP: parse(content)
    MP-->>-MC: data: dict
    
    MC->>+JW: write(data)
    JW-->>-MC: void
    
    %% Validation flow
    MC->>+V: validate(data)
    
    %% Schema validation
    V->>+SV: validate(data)
    SV->>EF: format_type_error/format_missing_field_error
    EF-->>SV: formatted error message
    SV-->>-V: is_valid: bool, error: Optional[ValidationError]
    
    %% Content validation
    V->>+CV: validate(data)
    CV->>EF: format_type_error/format_empty_error
    EF-->>CV: formatted error message
    CV-->>-V: is_valid: bool, error: Optional[ValidationError]
    
    %% Structure validation
    V->>+StV: validate(data)
    StV->>EF: format_structure_error
    EF-->>StV: formatted error message
    StV-->>-V: is_valid: bool, error: Optional[ValidationError]
    
    V-->>-MC: is_valid: bool, errors: str

    %% Save to database if enabled
    alt save_to_db is true
        MC->>+DB: insert_document(source_file)
        DB-->>-MC: document_id: int
        
        MC->>+DB: insert_json_output(document_id, data)
        DB-->>-MC: void
        
        MC->>+DB: insert_section(document_id, None, root_section)
        Note over MC,DB: Recursively inserts all child sections
        DB-->>-MC: void
        
        MC->>+DB: insert_validation_result(document_id, is_valid, errors)
        DB-->>-MC: void
    end

    MC-->>-User: output_path: str
```

## Component Documentation

### Validation System

The validation system follows the Strategy pattern with three main validators:

1. **Schema Validator**
   - Validates document structure against defined schema
   - Checks field presence and types
   - Ensures required fields exist

2. **Content Validator**
   - Validates content values
   - Checks for empty/invalid content
   - Ensures content format compliance

3. **Structure Validator**
   - Validates document hierarchy
   - Ensures proper section nesting
   - Validates level relationships

### Error Handling

The system uses a unified error handling approach:

1. **Error Formatter**
   - Provides consistent error message formatting
   - Supports multiple error types
   - Includes context in error messages

2. **Validation Error**
   - Encapsulates error information
   - Provides detailed error context
   - Supports error propagation

## Installation & Setup

### Prerequisites
- Python 3.8+
- PostgreSQL 13+
- Required Python packages:
  ```bash
  pip install -r requirements.txt
  ```

### Database Setup
1. Create PostgreSQL database:
   ```sql
   CREATE DATABASE mcp;
   ```

2. Configure environment:
   ```bash
   # Linux/macOS
   export DB_HOST=localhost
   export DB_PORT=5432
   export DB_NAME=mcp
   export DB_USER=your_username
   export DB_PASSWORD=your_password

   # Windows
   set DB_HOST=localhost
   set DB_PORT=5432
   set DB_NAME=mcp
   set DB_USER=your_username
   set DB_PASSWORD=your_password
   ```

3. Initialize database:
   ```bash
   python database/import_schema.py
   ```

## Usage Guide

### Basic Usage
```python
from markdown_converter import MarkdownConverter

# Initialize converter
converter = MarkdownConverter(
    source_file="path/to/markdown.md",
    save_to_db=True
)

# Convert and save
output_path = converter.convert()
```

### Advanced Usage
```python
# Custom output path
converter = MarkdownConverter(
    source_file="input.md",
    output_path="custom/path/output.json",
    save_to_db=True
)

# Convert with validation
output_path = converter.convert()
```

## Development Guide

### Project Structure
```
markdown_converter/
├── __init__.py
├── markdown_converter.py
├── validators/
│   ├── base/
│   │   ├── base_validator.py
│   │   └── error_handler.py
│   ├── schema_validator.py
│   ├── content_validator.py
│   └── structure_validator.py
└── database/
    ├── base_handler.py
    └── handlers/
```

### Adding New Validators
1. Extend `ValidationStrategy`
2. Implement `validate()` method
3. Use `ErrorFormatter` for messages
4. Register in `Validator` class

## Testing

### Unit Tests
```bash
python -m pytest tests/
```

### Integration Tests
```bash
python run_tests.py
```

## Contributing
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## License & Contact

### License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Contact
- **Author**: Tariq Ahmed
- **Email**: t.ahmed@stride.ae
- **Organization**: Stride Information Technology
