from config import client, MODEL


QUESTION = (
    "I have Rs. 2,000. "
    "I buy a book for Rs. 750. "
    "After buying the book, I spend 20% of the remaining money "
    "on stationery. "
    "How much money is left?"
)


response = client.chat.completions.create(

    model=MODEL,

    messages=[
        {
            "role": "system",
            "content": (
                "Solve the problem carefully. "
                "Give a concise reasoning summary and the final answer. "
                "Do not reveal private chain-of-thought."
            )
        },
        {
            "role": "user",
            "content": QUESTION
        }
    ],

    temperature=0
)


print("=== Chain-of-Thought Style Reasoning ===")

print("Question:")
print(QUESTION)

print("\nAnswer:")
print(response.choices[0].message.content)
