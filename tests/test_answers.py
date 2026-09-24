import sys
import os

# Project root
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

# Add project root and src
sys.path.append(PROJECT_ROOT)
sys.path.append(
    os.path.join(PROJECT_ROOT, "src")
)

from query_engine import QueryEngine


engine = QueryEngine()


test_cases = [

    {
        "question": "What are the working hours at Nova Corp?",
        "expected": [
            "9:00 AM",
            "6:00 PM",
            "Monday",
            "Friday"
        ]
    },

    {
        "question": "How many days before leave should I apply?",
        "expected": [
            "three",
            "3",
            "working days"
        ]
    },

    {
        "question": "How many employees are there?",
        "expected": [
            "100"
        ]
    },

    {
        "question": "What happens if I arrive late?",
        "expected": [
            "late",
            "attendance"
        ]
    },

    {
        "question": "What is the sick leave policy?",
        "expected": [
            "sick",
            "leave"
        ]
    },

    {
        "question": "What is the work from home policy?",
        "expected": [
            "work from home",
            "manager"
        ]
    }
]


passed = 0


print("\n")
print("=" * 70)
print("ARES-RAG X ANSWER QUALITY EVALUATION")
print("=" * 70)


for index, test in enumerate(test_cases, start=1):

    question = test["question"]

    print("\n")
    print("-" * 70)
    print(f"TEST {index}")
    print("-" * 70)

    print("Question:")
    print(question)

    answer = engine.answer_query(question)

    print("\nAnswer:")
    print(answer)

    answer_lower = answer.lower()

    matched = []

    for keyword in test["expected"]:

        if keyword.lower() in answer_lower:
            matched.append(keyword)

    # Pass if at least one expected concept is found
    if len(matched) >= 1:

        passed += 1

        print("\nRESULT: PASS")
        print("Matched:", matched)

    else:

        print("\nRESULT: FAIL")
        print("Expected:", test["expected"])


total = len(test_cases)

pass_rate = (
    passed / total
) * 100


print("\n")
print("=" * 70)
print("FINAL ANSWER EVALUATION")
print("=" * 70)

print(f"Total Questions : {total}")
print(f"Passed          : {passed}")
print(f"Pass Rate       : {pass_rate:.2f}%")

print("=" * 70)
