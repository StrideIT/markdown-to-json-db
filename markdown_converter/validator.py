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
        try:
            jsonschema.validate(instance=data, schema=self.schema)
            return True, ""
        except ValidationError as e:
            return False, str(e)
