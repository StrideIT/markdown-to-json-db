classDiagram
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

    class Validator {
        -schema: dict
        +__init__()
        +validate(data: dict)
    }

    class MarkdownConverter {
        -source_file: str
        -output_path: Optional[str]
        -file_reader: FileReader
        -json_writer: JSONWriter
        -validator: Validator
        +__init__(source_file: str, output_path: Optional[str] = None)
        +convert() str
        -_default_output_path() str
        -_parse_markdown(content: List[str]) dict
    }

    MarkdownConverter --> FileReader
    MarkdownConverter --> JSONWriter
    MarkdownConverter --> Validator
