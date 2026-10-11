
"""ReAct agent that finds book combinations within a budget."""

import json

from config import client, MODEL
from tools import TOOLS, TOOL_FUNCTIONS


SYSTEM_PROMPT = """
You are a book-shopping assistant.
The budget is Rs. 1,200.
The only available books are:
- Python Basics
- Data Structures
- Machine Learning

Always use get_book_price to retrieve prices.
Use calculator to calculate book combinations.
Find every pair of different books that costs no more than Rs. 1,200.
Explain which pairs fit and which exceed the budget.
"""


QUESTION = (
    "I have Rs. 1,200. Which two books can I buy together within my "
    "budget? The available books are exactly Python Basics, "
    "Data Structures, and Machine Learning."
)


def run_react_agent(question, max_steps=10):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]

    for step in range(1, max_steps + 1):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0,
        )

        message = response.choices[0].message

        if not message.tool_calls:
            return message.content or "No final answer returned."

        messages.append({
            "role": "assistant",
            "content": message.content or "",
            "tool_calls": [
                {
                    "id": call.id,
                    "type": "function",
                    "function": {
                        "name": call.function.name,
                        "arguments": call.function.arguments or "{}",
                    },
                }
                for call in message.tool_calls
            ],
        })

        for call in message.tool_calls:
            name = call.function.name
            arguments = json.loads(call.function.arguments or "{}")

            print(f"\n[Action] {name}({arguments})")

            function = TOOL_FUNCTIONS.get(name)
            if function is None:
                result = f"Unknown tool: {name}"
            else:
                try:
                    result = function(**arguments)
                except Exception as exc:
                    result = f"Tool error: {exc}"

            print(f"[Observation] {result}")

            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": str(result),
            })

    return "Stopped: maximum steps reached."


if __name__ == "__main__":
    print("=== ReAct Agent ===")
    print("Question:")
    print(QUESTION)
    print()

    answer = run_react_agent(QUESTION)
    print("\nFinal Answer:\n")
    print(answer)
