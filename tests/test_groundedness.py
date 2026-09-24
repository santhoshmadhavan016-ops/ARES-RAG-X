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
from retriever import retrieve_and_rerank


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
            "3",
            "three",
            "working days"
        ]
    },

    {
        "question": "What is the work from home policy?",
        "expected": [
            "work from home",
            "manager"
        ]
    },

    {
        "question": "What happens if I arrive late?",
        "expected": [
            "late",
            "attendance"
        ]
    }
]


passed = 0


print("\n")
print("=" * 70)
print("ARES-RAG X GROUNDEDNESS EVALUATION")
print("=" * 70)


for index, test in enumerate(test_cases, start=1):

    question = test["question"]

    print("\n")
    print("-" * 70)
    print(f"TEST {index}")
    print("-" * 70)

    print("Question:")
    print(question)

    # Retrieve source documents
    rag_results = retrieve_and_rerank(
        question,
        top_k=3
    )

    # Generate final answer
    answer = engine.answer_query(question)

    print("\nGenerated Answer:")
    print(answer)

    # Combine retrieved documents
    source_text = ""

    for result in rag_results:

        source_text += " " + result["document"]

    source_text = source_text.lower()
    answer_lower = answer.lower()

    # Check whether answer concepts exist in source
    matched = []

    for expected in test["expected"]:

        expected_lower = expected.lower()

        if expected_lower in answer_lower:
            if expected_lower in source_text:
                matched.append(expected)

    if len(matched) >= 1:

        passed += 1

        print("\nGroundedness: PASS")
        print("Supported concepts:", matched)

    else:

        print("\nGroundedness: FAIL")
        print("No expected concepts were confirmed in the source.")


total = len(test_cases)

groundedness_rate = (
    passed / total
) * 100


print("\n")
print("=" * 70)
print("FINAL GROUNDEDNESS RESULTS")
print("=" * 70)

print(f"Total Questions       : {total}")
print(f"Grounded Answers      : {passed}")
print(f"Groundedness Rate     : {groundedness_rate:.2f}%")

print("=" * 70)
