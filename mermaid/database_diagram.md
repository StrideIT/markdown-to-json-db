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

    %% Notes on validation
    %% - errors field in VALIDATION_RESULT stores formatted messages from:
    %%   1. SchemaValidator (field presence and types)
    %%   2. ContentValidator (content validity)
    %%   3. StructureValidator (section hierarchy)
    %% - Messages are formatted through ErrorFormatter for consistency
    %% - Multiple validation errors can be stored as concatenated text
