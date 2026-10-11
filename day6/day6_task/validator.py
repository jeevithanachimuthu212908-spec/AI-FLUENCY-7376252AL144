# validator.py

from tools import SCHEMAS


def validate_arguments(tool_name, arguments):

    # 1. Check whether tool exists
    if tool_name not in SCHEMAS:
        return f"Unknown tool: {tool_name}"

    schema = SCHEMAS[tool_name]

    # 2. Arguments must be a dictionary
    if not isinstance(arguments, dict):
        return "Arguments must be a JSON object."

    properties = schema["properties"]

    # 3. Check required arguments
    for required_field in schema["required"]:
        if required_field not in arguments:
            return (
                f"Missing required argument: '{required_field}'. "
                f"Expected fields: {list(properties.keys())}"
            )

    # 4. Check invented/extra arguments
    if schema["additionalProperties"] is False:
        for argument in arguments:
            if argument not in properties:
                return (
                    f"Unexpected argument: '{argument}'. "
                    f"Allowed arguments: {list(properties.keys())}"
                )

    # 5. Check data types
    for argument, value in arguments.items():

        expected_type = properties[argument]["type"]

        if expected_type == "integer":
            if not isinstance(value, int) or isinstance(value, bool):
                return f"Wrong type for '{argument}'. Expected integer."

        elif expected_type == "string":
            if not isinstance(value, str):
                return f"Wrong type for '{argument}'. Expected string."

    # 6. Check enum values
    for argument, value in arguments.items():

        if "enum" in properties[argument]:

            allowed_values = properties[argument]["enum"]

            if value not in allowed_values:
                return (
                    f"Invalid value for '{argument}'. "
                    f"Expected one of {allowed_values}."
                )

    # 7. Business-rule validation
    if tool_name == "calculate_attendance":

        present = arguments["present_classes"]
        total = arguments["total_classes"]

        if present < 0:
            return "Invalid value: present_classes cannot be negative."

        if total <= 0:
            return "Invalid value: total_classes must be greater than 0."

        if present > total:
            return "Invalid value: present_classes cannot be greater than total_classes."

    return None
