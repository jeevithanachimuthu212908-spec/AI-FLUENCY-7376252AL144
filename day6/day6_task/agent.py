# agent.py

import os
import json
from openai import OpenAI
from dotenv import load_dotenv

from tools import TOOLS
from tools import calculate_attendance
from tools import get_subject_info

from validator import validate_arguments


load_dotenv()


client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


MODEL = os.getenv("MODEL")


# --------------------------------
# Tool execution
# --------------------------------

def execute_tool(tool_name, arguments):

    if tool_name == "calculate_attendance":

        return calculate_attendance(
            arguments["present_classes"],
            arguments["total_classes"]
        )

    elif tool_name == "get_subject_info":

        return get_subject_info(
            arguments["subject"],
            arguments["type"]
        )

    return f"Unknown tool: {tool_name}"


# --------------------------------
# Agent
# --------------------------------

def run_agent(user_question):

    messages = [
        {
            "role": "system",
            "content": (
                "You are a college student assistant. "
                "Use tools when necessary. "
                "Do not invent tool arguments."
            )
        },
        {
            "role": "user",
            "content": user_question
        }
    ]

    max_steps = 5
    previous_calls = []

    max_tokens = 500

    for step in range(max_steps):

        print(f"\n--- Step {step + 1} ---")

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            max_tokens=max_tokens
        )

        message = response.choices[0].message
        finish_reason = response.choices[0].finish_reason

        print("finish_reason:", finish_reason)

        # --------------------------------
        # If response was truncated
        # --------------------------------

        if finish_reason == "length":

            print("Response was truncated. Retrying...")

            max_tokens *= 2
            continue

        # --------------------------------
        # Normal final response
        # --------------------------------

        if finish_reason == "stop":

            return message.content

        # --------------------------------
        # Tool calls
        # --------------------------------

        if finish_reason == "tool_calls":

            messages.append(message)

            current_calls = []

            for tool_call in message.tool_calls:

                tool_name = tool_call.function.name
                raw_arguments = tool_call.function.arguments

                print("Tool:", tool_name)
                print("Arguments:", raw_arguments)

                current_calls.append(
                    tool_name + "|" + raw_arguments
                )

                # --------------------------------
                # Repeated identical call check
                # --------------------------------

                if current_calls.count(
                    tool_name + "|" + raw_arguments
                ) > 1:

                    return "Stopped: repeated identical tool call."

                # --------------------------------
                # Parse JSON
                # --------------------------------

                try:

                    arguments = json.loads(raw_arguments)

                except json.JSONDecodeError:

                    error_message = (
                        "Invalid JSON arguments. "
                        "Please return valid JSON."
                    )

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": error_message
                    })

                    continue

                # --------------------------------
                # Validate
                # --------------------------------

                validation_error = validate_arguments(
                    tool_name,
                    arguments
                )

                if validation_error:

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": validation_error
                    })

                    continue

                # --------------------------------
                # Execute
                # --------------------------------

                try:

                    result = execute_tool(
                        tool_name,
                        arguments
                    )

                except Exception as error:

                    result = f"Tool execution failed: {error}"

                # --------------------------------
                # Return result to model
                # --------------------------------

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                })

            continue

    return "Stopped: maximum number of steps reached."


# --------------------------------
# Test
# --------------------------------

if __name__ == "__main__":

    question = input("Ask your question: ")

    answer = run_agent(question)

    print("\nFinal Answer:")
    print(answer)
    