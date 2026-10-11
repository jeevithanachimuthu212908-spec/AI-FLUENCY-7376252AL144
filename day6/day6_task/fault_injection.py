# fault_injection.py

from validator import validate_arguments


tests = [

    (
        "Invalid JSON",
        "calculate_attendance",
        "not valid json"
    ),

    (
        "Unknown tool",
        "calculate_marks",
        {}
    ),

    (
        "Missing argument",
        "calculate_attendance",
        {
            "present_classes": 40
        }
    ),

    (
        "Wrong type",
        "calculate_attendance",
        {
            "present_classes": "40",
            "total_classes": 50
        }
    ),

    (
        "Invalid enum",
        "get_subject_info",
        {
            "subject": "DSA",
            "type": "sports"
        }
    ),

    (
        "Invented argument",
        "get_subject_info",
        {
            "subject": "DSA",
            "type": "lab",
            "college": "BIT"
        }
    ),

    (
        "Negative classes",
        "calculate_attendance",
        {
            "present_classes": -5,
            "total_classes": 50
        }
    ),

    (
        "Zero total classes",
        "calculate_attendance",
        {
            "present_classes": 10,
            "total_classes": 0
        }
    )
]


for name, tool_name, arguments in tests:

    print("\n----------------------------")
    print("Test:", name)
    print("Tool:", tool_name)
    print("Arguments:", arguments)

    # Invalid JSON is handled separately
    if name == "Invalid JSON":

        import json

        try:
            parsed = json.loads(arguments)

            result = validate_arguments(
                tool_name,
                parsed
            )

        except json.JSONDecodeError:
            result = "Invalid JSON arguments."

    else:

        result = validate_arguments(
            tool_name,
            arguments
        )

    if result is None:
        print("Result: VALID")

    else:
        print("Result:", result)
        