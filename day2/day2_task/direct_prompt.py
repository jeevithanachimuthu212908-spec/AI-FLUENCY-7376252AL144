from config import client, MODEL


QUESTION = (
    "I have Rs. 1,200. "
    "Which two books can I buy together within my budget? "
    "The book prices are: "
    "Python Basics = Rs. 450, "
    "Data Structures = Rs. 600, "
    "Machine Learning = Rs. 750."
)


response = client.chat.completions.create(

    model=MODEL,

    messages=[
        {
            "role": "user",
            "content": QUESTION
        }
    ],

    temperature=0
)


print("=== Direct Prompting ===")

print("Question:")
print(QUESTION)

print("\nAnswer:")
print(response.choices[0].message.content)
