from config import client, MODEL, COURSE_FEES

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": f"""
You are a college course fee assistant.

Here is the official course fee information:

{COURSE_FEES}

Use this information to answer questions about course fees.
If the user asks about a course that is listed, give the correct fee.
Do not say you don't have the information when the course is present in the provided data.
"""
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        temperature=0.7
    )

    print("Bot:", response.choices[0].message.content)