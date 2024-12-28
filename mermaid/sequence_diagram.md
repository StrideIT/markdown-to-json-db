sequenceDiagram
    participant User
    participant MarkdownConverter
    participant FileReader
    participant JSONWriter
    participant Validator
    participant Database

    User->>MarkdownConverter: convert()
    MarkdownConverter->>FileReader: read()
    FileReader-->>MarkdownConverter: content
    MarkdownConverter->>MarkdownConverter: _parse_markdown(content)
    MarkdownConverter->>JSONWriter: write(data)
    JSONWriter-->>MarkdownConverter: 
    MarkdownConverter->>Validator: validate(data)
    Validator-->>MarkdownConverter: 
    MarkdownConverter->>Database: store(output_file)
    Database-->>MarkdownConverter: 
    MarkdownConverter-->>User: output_file
