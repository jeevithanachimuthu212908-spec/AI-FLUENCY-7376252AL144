import json


def get_courses():
    """Return all courses from the private course database."""
    with open("data/courses.json", "r", encoding="utf-8") as file:
        return json.load(file)


def find_course_pairs(budget):
    """Find pairs of courses whose combined fee is within the budget."""
    courses = get_courses()
    pairs = []

    for i in range(len(courses)):
        for j in range(i + 1, len(courses)):
            total = courses[i]["fee"] + courses[j]["fee"]

            if total <= budget:
                pairs.append({
                    "course1": courses[i]["name"],
                    "course2": courses[j]["name"],
                    "total_fee": total
                })

    return pairs
    