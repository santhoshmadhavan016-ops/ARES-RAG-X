import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.retriever import retrieve_and_rerank


# ============================================================
# RETRIEVAL EVALUATION DATASET
# ============================================================

test_cases = [

    {
        "query": "What are the working hours at Nova Corp?",
        "expected_file": "employee_handbook.txt"
    },

    {
        "query": "How many days before leave should I apply?",
        "expected_file": "leave_policy.txt"
    },

    {
        "query": "What happens if I arrive late?",
        "expected_file": "attendance_policy.txt"
    },

    {
        "query": "What is the sick leave policy?",
        "expected_file": "leave_policy.txt"
    },

    {
        "query": "Can employees work from home?",
        "expected_file": "work_from_home_policy.txt"
    },

    {
        "query": "What are the rules for remote access?",
        "expected_file": "remote_access_policy.txt"
    },

    {
        "query": "How should company data be classified?",
        "expected_file": "information_classification_policy.txt"
    },

    {
        "query": "What is the employee onboarding process?",
        "expected_file": "employee_onboarding_policy.txt"
    },

    {
        "query": "What happens when an employee leaves the company?",
        "expected_file": "employee_offboarding_policy.txt"
    },

    {
        "query": "What are the rules for company assets?",
        "expected_file": "asset_management_policy.txt"
    }
]


# ============================================================
# EVALUATION
# ============================================================

top1_correct = 0
top3_correct = 0
top5_correct = 0


print("=" * 70)
print("ARES-RAG X - RETRIEVAL EVALUATION")
print("=" * 70)


for i, test in enumerate(test_cases, start=1):

    query = test["query"]
    expected_file = test["expected_file"]

    results = retrieve_and_rerank(
        query,
        top_k=5
    )

    retrieved_files = [
        result["metadata"]["filename"]
        for result in results
    ]

    top1 = expected_file in retrieved_files[:1]
    top3 = expected_file in retrieved_files[:3]
    top5 = expected_file in retrieved_files[:5]

    if top1:
        top1_correct += 1

    if top3:
        top3_correct += 1

    if top5:
        top5_correct += 1


    print("\n" + "-" * 70)

    print(f"TEST {i}")
    print(f"Query: {query}")

    print(f"Expected: {expected_file}")

    print("Retrieved:")

    for rank, filename in enumerate(
        retrieved_files,
        start=1
    ):
        print(f"  {rank}. {filename}")

    print(f"Top-1: {'PASS' if top1 else 'FAIL'}")
    print(f"Top-3: {'PASS' if top3 else 'FAIL'}")
    print(f"Top-5: {'PASS' if top5 else 'FAIL'}")


# ============================================================
# FINAL METRICS
# ============================================================

total = len(test_cases)

top1_accuracy = (
    top1_correct / total
) * 100

top3_accuracy = (
    top3_correct / total
) * 100

top5_accuracy = (
    top5_correct / total
) * 100


print("\n")
print("=" * 70)
print("FINAL RETRIEVAL RESULTS")
print("=" * 70)

print(f"Total Questions : {total}")

print(
    f"Top-1 Accuracy  : {top1_accuracy:.2f}%"
)

print(
    f"Top-3 Accuracy  : {top3_accuracy:.2f}%"
)

print(
    f"Top-5 Accuracy  : {top5_accuracy:.2f}%"
)

print("=" * 70)