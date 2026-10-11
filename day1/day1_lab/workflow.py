import re

COURSE_FEES = {
    "CS101": 12000,
    "AI202": 18000,
    "DS303": 15000
}


def get_course_fee(course_code):
    return COURSE_FEES.get(course_code.upper())


def workflow(user_input):
    match = re.search(r"(CS101|AI202|DS303)", user_input.upper())

    if match:
        course_code = match.group(1)
        fee = get_course_fee(course_code)

        return f"The fee for {course_code} is ₹{fee}."

    return "Sorry, I can only answer course fee questions."


if __name__ == "__main__":
    while True:
        question = input("You: ")

        if question.lower() == "exit":
            break

        print("Workflow:", workflow(question))
        