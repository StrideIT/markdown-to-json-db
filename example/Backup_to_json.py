import json
import os
import re
from typing import Optional, List, Dict, Any
from jsonschema.exceptions import ValidationError

class MarkdownConverter:
    def __init__(self, source_file: str, output_path: Optional[str] = None):
        """
        Initialize the converter with source file and optional output path.
        
        Args:
            source_file (str): Path to the source markdown file
            output_path (Optional[str]): Path where the JSON file should be saved. 
                                       If not provided, uses source directory.
        """
        self.source_file = source_file
        if output_path is None:
            # Use source directory with modified filename
            source_dir = os.path.dirname(source_file)
            source_filename = os.path.splitext(os.path.basename(source_file))[0]
            self.output_path = os.path.join(source_dir, f"{source_filename}.json")
        else:
            self.output_path = output_path

    def convert(self) -> str:
        """
        Convert markdown file to JSON and save it.
        
        Returns:
            str: Path to the created JSON file
        """
        # Read markdown file
        with open(self.source_file, 'r', encoding='utf-8') as f:
            content = f.readlines()

        # Initialize tracking
        stack: List[Dict[str, Any]] = []  # Track current path in hierarchy
        current_content: List[str] = []

        for line in content:
            line = line.strip()
            if not line:
                continue

            # Check if line is a heading
            heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if heading_match:
                # Save any accumulated content
                if current_content and stack:
                    stack[-1]["content"] = "\n".join(current_content)
                current_content = []

                level = len(heading_match.group(1))
                title = heading_match.group(2)

                # Create new node
                new_node = {
                    "title": title,
                    "content": "",
                    "level": level,
                    "children": []
                }

                # Level 1 headings go to root
                if level == 1:
                    if self.first_level_1 is None:
                        self.first_level_1 = new_node
                        self.root.append(self.first_level_1)
                        stack = [new_node]
                    else:
                        self.first_level_1["children"].append(new_node)
                        stack = [new_node]
                    continue

                # Pop back to find appropriate parent
                while stack and stack[-1]["level"] >= level:
                    stack.pop()

                # Add to parent if we have one
                if stack:
                    # Find closest parent with lower level
                    parent = stack[-1]
                    parent["children"].append(new_node)
                else:
                    # No parent found, add to root
                    self.root.append(new_node)

                # Add to stack
                stack.append(new_node)
            else:
                # Add to current content
                current_content.append(line)

        # Handle any remaining content
        if current_content and stack:
            stack[-1]["content"] = "\n".join(current_content)

        # Create output directory if needed
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

        # Save to JSON file
        with open(self.output_path, 'w', encoding='utf-8') as f:
            json.dump({os.path.basename(self.source_file): self.root}, f, indent=2)

        return self.output_path

    def process(self) -> str:
        """
        Main processing method.
        
        Returns:
            str: Path to the created JSON file
            
        Raises:
            FileNotFoundError: If source file doesn't exist
            Exception: If any other error occurs during processing
        """
        try:
            # Validate source file
            if not os.path.exists(self.source_file):
                raise FileNotFoundError(f"Source file not found: {self.source_file}")

            # Initialize root structure
            self.root: List[Dict[str, Any]] = []
            self.first_level_1: Optional[Dict[str, Any]] = None

            # Convert and save
            output_path = self.convert()
            return output_path

        except Exception as e:
            raise Exception(f"Error processing file: {str(e)}")

def main():
    # Example usage
    import glob
    import jsonschema

    # Define a simple JSON schema for validation
    schema = {
        "type": "object",
        "patternProperties": {
            ".*": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "content": {"type": "string"},
                        "level": {"type": "integer"},
                        "children": {"type": "array"}
                    },
                    "required": ["title", "level", "children"]
                }
            }
        }
    }

    md_files = glob.glob('example/*.md')
    for md_file in md_files:
        output_file = None
        try:
            print(f"\nProcessing {md_file}")
            converter = MarkdownConverter(md_file)
            output_file = converter.process()
            print(f'JSON file has been created successfully: {output_file}')

            # Validate the generated JSON file
            with open(output_file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
                jsonschema.validate(instance=json_data, schema=schema)
            print(f'JSON file {output_file} is valid.')

        except ValidationError as ve:
            print(f"JSON validation error in {output_file}: {ve.message}")
        except Exception as e:
            print(f"Error processing {md_file}: {str(e)}")

if __name__ == '__main__':
    main()
