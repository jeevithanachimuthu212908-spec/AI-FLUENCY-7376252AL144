import os
import json
from dotenv import load_dotenv
from groq import Groq
from tools import find_course_pairs

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

tools = [
    {
        "type": "function",
        "function": {
            "name": "find_course_pairs",
            "description": "Find pairs of courses whose combined fee is within a given budget.",
            "parameters": {
                "type": "object",
                "properties": {
                    "budget": {
                        "type": "number",
                        "description": "Maximum total budget for two courses."
                    }
                },
                "required": ["budget"]
            }
        }
    }
]

messages = [
    {
        "role": "system",
        "content": (
            "You are an AI course advisor. "
            "Use the available tool whenever the user asks about "
            "course combinations, fees, or budgets. "
            "Do not invent course information."
        )
    }
]

print("=== AI Agent ===")
print("Type 'exit' to stop.")

while True:
    user_input = input("\nYou: ")

    if user_input.lower() == "exit":
        break

    messages.append({
        "role": "user",
        "content": user_input
    })

    # LLM decides whether a tool is needed
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    assistant_message = response.choices[0].message
    messages.append(assistant_message)

    # Tool selection
    if assistant_message.tool_calls:

        print("\n[LLM decided to use a tool]")

        for tool_call in assistant_message.tool_calls:

            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            print(f"[Tool selected: {tool_name}]")
            print(f"[Tool arguments: {arguments}]")

            # Execute the selected tool
            if tool_name == "find_course_pairs":
                result = find_course_pairs(arguments["budget"])

                print("[Private data accessed through tool]")
                print("[Tool result received]")

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })

        # LLM observes the tool result and creates final answer
        final_response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages
        )

        final_message = final_response.choices[0].message.content

        messages.append({
            "role": "assistant",
            "content": final_message
        })

        print("\n[LLM processed the tool result]")
        print("\nAgent:", final_message)

    else:
        print("\nAgent:", assistant_message.content)
        