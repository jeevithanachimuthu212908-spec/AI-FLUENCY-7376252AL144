# structured_demo.py

import os
import json

from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()


client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

MODEL = os.getenv("MODEL")


question = """
Extract the following student information:

Jayasree is an IT student.
She has completed 42 classes out of 50.
Her current subject is DSA.
Her class type is lab.
"""


# ==========================================
# 1. NO CONSTRAINT
# ==========================================

print("\n========== 1. NO CONSTRAINT ==========")

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {
            "role": "user",
            "content": question
        }
    ],
    max_tokens=300
)

raw_reply = response.choices[0].message.content

print("Raw reply:")
print(raw_reply)


# ==========================================
# 2. JSON MODE
# ==========================================

print("\n========== 2. JSON MODE ==========")

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {
            "role": "system",
            "content": "Return the extracted information as JSON."
        },
        {
            "role": "user",
            "content": question
        }
    ],
    response_format={
        "type": "json_object"
    },
    max_tokens=300
)

raw_reply = response.choices[0].message.content

print("Raw reply:")
print(raw_reply)

try:
    parsed = json.loads(raw_reply)

    print("\nParsed result:")
    print(parsed)

except json.JSONDecodeError as e:

    print("\nJSON parsing error:")
    print(e)


# ==========================================
# 3. SCHEMA MODE
# ==========================================

print("\n========== 3. SCHEMA MODE ==========")

student_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string"
        },
        "branch": {
            "type": "string"
        },
        "present_classes": {
            "type": "integer"
        },
        "total_classes": {
            "type": "integer"
        },
        "subject": {
            "type": "string"
        },
        "class_type": {
            "type": "string",
            "enum": [
                "theory",
                "lab"
            ]
        }
    },
    "required": [
        "name",
        "branch",
        "present_classes",
        "total_classes",
        "subject",
        "class_type"
    ],
    "additionalProperties": False
}


try:

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "Extract the student information from the given sentence."
            },
            {
                "role": "user",
                "content": question
            }
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "student_information",
                "strict": True,
                "schema": student_schema
            }
        },
        max_tokens=300
    )

    raw_reply = response.choices[0].message.content

    print("Raw reply:")
    print(raw_reply)

    parsed = json.loads(raw_reply)

    print("\nParsed result:")
    print(parsed)

except Exception as e:

    print("\nSchema mode error:")
    print(e)
    