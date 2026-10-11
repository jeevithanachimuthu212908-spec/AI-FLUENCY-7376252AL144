# tools.py

# -----------------------------
# Tool 1: Calculate Attendance
# -----------------------------

def calculate_attendance(present_classes, total_classes):
    if total_classes <= 0:
        return "Error: total_classes must be greater than 0."

    attendance = (present_classes / total_classes) * 100

    return f"Attendance is {attendance:.2f}%."


# -----------------------------
# Tool 2: Get Subject Information
# -----------------------------

SUBJECTS = {
    "Java": {
        "faculty": "Dr. Kumar",
        "room": "LC-3",
        "type": "theory"
    },

    "DSA": {
        "faculty": "Ms. Priya",
        "room": "LC-4",
        "type": "lab"
    },

    "SQL": {
        "faculty": "Mr. Arun",
        "room": "Lab-2",
        "type": "lab"
    }
}


def get_subject_info(subject, type):
    if subject not in SUBJECTS:
        return f"Subject '{subject}' was not found."

    information = SUBJECTS[subject]

    if information["type"] != type:
        return f"{subject} is a {information['type']} subject, not {type}."

    return (
        f"Subject: {subject}, "
        f"Faculty: {information['faculty']}, "
        f"Room: {information['room']}, "
        f"Type: {information['type']}"
    )


# -----------------------------
# Schemas
# -----------------------------

SCHEMAS = {

    "calculate_attendance": {
        "type": "object",
        "properties": {
            "present_classes": {
                "type": "integer"
            },
            "total_classes": {
                "type": "integer"
            }
        },
        "required": [
            "present_classes",
            "total_classes"
        ],
        "additionalProperties": False
    },

    "get_subject_info": {
        "type": "object",
        "properties": {
            "subject": {
                "type": "string"
            },
            "type": {
                "type": "string",
                "enum": [
                    "theory",
                    "lab"
                ]
            }
        },
        "required": [
            "subject",
            "type"
        ],
        "additionalProperties": False
    }
}


# -----------------------------
# Tool definitions sent to LLM
# -----------------------------

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculate_attendance",
            "description": "Calculate a student's attendance percentage.",
            "parameters": SCHEMAS["calculate_attendance"]
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_subject_info",
            "description": "Get faculty, room and type information about a college subject.",
            "parameters": SCHEMAS["get_subject_info"]
        }
    }
]
