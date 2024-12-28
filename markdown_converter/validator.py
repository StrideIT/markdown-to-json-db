import jsonschema
from jsonschema.exceptions import ValidationError

"""
Author: Tariq Ahmed
Email: t.ahmed@stride.ae
Organization: Stride Information Technology

This module provides the Validator class for validating JSON content against a schema.
"""

class Validator:
    def __init__(self):
        """
        Initialize the Validator with a predefined JSON schema.
        """
        self.schema = {
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

    def validate(self, data: dict):
        """
        Validate the JSON data against the predefined schema.

        Args:
            data (dict): The JSON data to be validated.

        Returns:
            Tuple[bool, str]: A tuple containing a boolean indicating if the data is valid and an error message if invalid.
        """
        try:
            jsonschema.validate(instance=data, schema=self.schema)
            return True, ""
        except ValidationError as e:
            return False, str(e)
