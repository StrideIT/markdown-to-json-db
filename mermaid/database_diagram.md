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
    DOCUMENT ||--o{ VALIDATION_RESULT : "has many"
