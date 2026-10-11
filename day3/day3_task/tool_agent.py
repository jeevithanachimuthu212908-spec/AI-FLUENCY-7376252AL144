import os
from groq import Groq

from tool import read_notice


client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


tools = [
    {
        "type": "function",
        "function": {
            "name": "read_notice",
            "description": "Reads the college fee notice and returns the course fees and scholarship information.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]


question = """
What are the fees for CS101 and AI202 after the 20% merit scholarship?

Use the available tool if you need the actual fee information.
"""


messages = [
    {
        "role": "user",
        "content": question
    }
]


print("\n=== LLM WITH ONE TOOL ===")

print("\nQuestion:")
print(question.strip())


response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)


message = response.choices[0].message


if message.tool_calls:

    for tool_call in message.tool_calls:

        print("\nTool call:")
        print(f"Name: {tool_call.function.name}")
        print(f"Arguments: {tool_call.function.arguments}")

        if tool_call.function.name == "read_notice":

            tool_result = read_notice()

            print("\nTool result:")
            print(tool_result)

            messages.append(message)

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result
                }
            )


    final_response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages,
        tools=tools
    )

    print("\nFinal answer:")
    print(final_response.choices[0].message.content)


else:

    print("\nThe model did not call the tool.")

    print("\nFinal answer:")
    print(message.content)
    