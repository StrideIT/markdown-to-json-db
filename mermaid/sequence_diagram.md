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
