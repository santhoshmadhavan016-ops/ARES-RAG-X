import sys
import os

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(PROJECT_ROOT)
sys.path.append(
    os.path.join(PROJECT_ROOT, "src")
)

from query_engine import QueryEngine


engine = QueryEngine()


test_cases = [

    # SQL TEST 1
    {
        "question": "How many employees are there?",
        "expected": [
            ["100"]
        ]
    },

    # SQL TEST 2
    # Any ONE of these salary formats is acceptable
    {
        "question": "What is the average salary?",
        "expected": [
            ["90,202", "90202", "$90,202"]
        ]
    },

    # SQL TEST 3
    {
        "question": "How many departments are there?",
        "expected": [
            ["6"]
        ]
    },

    # HYBRID TEST 1
    {
        "question": (
            "How many employees are there, "
            "and what is the work from home policy?"
        ),
        "expected": [
            ["100"],
            ["work from home"],
            ["manager"]
        ]
    },

    # HYBRID TEST 2
    {
        "question": (
            "How many employees are there, "
            "and what does the employee handbook "
            "say about employee responsibilities?"
        ),
        "expected": [
            ["100"],
            ["employee"],
            ["responsibilities"]
        ]
    }
]


passed = 0


print("\n")
print("=" * 70)
print("ARES-RAG X SQL + HYBRID EVALUATION")
print("=" * 70)


for index, test in enumerate(
    test_cases,
    start=1
):

    question = test["question"]

    print("\n")
    print("-" * 70)
    print(f"TEST {index}")
    print("-" * 70)

    print("Question:")
    print(question)

    # Run QueryEngine
    answer = engine.answer_query(
        question
    )

    print("\nAnswer:")
    print(answer)

    answer_lower = answer.lower()

    matched = []
    failed = []

    # Each group contains acceptable alternatives
    for expected_group in test["expected"]:

        found = False

        for expected in expected_group:

            if expected.lower() in answer_lower:

                matched.append(expected)
                found = True
                break

        if not found:

            failed.append(
                expected_group
            )

    # PASS only if every required concept
    # has at least one matching alternative
    if len(failed) == 0:

        passed += 1

        print("\nRESULT: PASS")

        print(
            "Matched:",
            matched
        )

    else:

        print("\nRESULT: FAIL")

        print(
            "Expected:",
            test["expected"]
        )

        print(
            "Matched:",
            matched
        )

        print(
            "Missing:",
            failed
        )


# ==========================================================
# FINAL RESULTS
# ==========================================================

total = len(test_cases)

pass_rate = (
    passed / total
) * 100


print("\n")
print("=" * 70)
print("FINAL SQL + HYBRID EVALUATION")
print("=" * 70)

print(
    f"Total Tests : {total}"
)

print(
    f"Passed      : {passed}"
)

print(
    f"Pass Rate   : {pass_rate:.2f}%"
)

print("=" * 70)