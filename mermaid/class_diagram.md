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
