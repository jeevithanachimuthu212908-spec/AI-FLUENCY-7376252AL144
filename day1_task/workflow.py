import json
from itertools import combinations

# Load private course data
with open("data/courses.json", "r", encoding="utf-8") as file:
    courses = json.load(file)

budget = 30000

print("=== Rule-Based Course Workflow ===")
print(f"Budget: ₹{budget}")

# Fixed rule: check every pair of courses
valid_pairs = []

for course1, course2 in combinations(courses, 2):
    total_fee = course1["fee"] + course2["fee"]

    if total_fee <= budget:
        valid_pairs.append(
            (course1["name"], course2["name"], total_fee)
        )

print("\nCourses that can be taken together:")

for course1, course2, total_fee in valid_pairs:
    print(f"- {course1} + {course2} = ₹{total_fee}")