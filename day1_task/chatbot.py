import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

print("=== Plain Chatbot ===")
print("Type 'exit' to stop.")

while True:
    user_input = input("\nYou: ")

    if user_input.lower() == "exit":
        break

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful course advisor."
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    print("Bot:", response.choices[0].message.content)
    