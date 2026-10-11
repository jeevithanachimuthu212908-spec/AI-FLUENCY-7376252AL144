from config import client, MODEL


QUESTION = (
    "I have Rs. 2,000. "
    "I buy a book for Rs. 750. "
    "After buying the book, I spend 20% of the remaining money "
    "on stationery. "
    "How much money is left?"
)


def ask_model(temperature):

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

        temperature=temperature
    )

    return response.choices[0].message.content


print("=== SELF-CONSISTENCY EXPERIMENT ===")

print("Question:")
print(QUESTION)


for run in range(1, 6):

    print(
        f"\n--- Run {run} | Temperature 0.8 ---"
    )

    print(
        ask_model(0.8)
    )


print("\n--- Temperature 0 ---")

print(
    ask_model(0)
)
