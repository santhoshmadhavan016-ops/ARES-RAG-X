import os
import sys
import importlib.util


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

APP_PATH = os.path.join(PROJECT_ROOT, "app")
SRC_PATH = os.path.join(PROJECT_ROOT, "src")

sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, APP_PATH)
sys.path.insert(0, SRC_PATH)


# ============================================================
# LOAD RAG AGENT
# ============================================================

rag_agent_path = os.path.join(APP_PATH, "rag_agent.py")

spec = importlib.util.spec_from_file_location(
    "rag_agent_module",
    rag_agent_path
)

rag_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rag_module)

RAGAgent = rag_module.RAGAgent


# ============================================================
# INITIALIZE RAG AGENT
# ============================================================

print("\n" + "=" * 75)
print("ARES-RAG X — RAG EVALUATION")
print("=" * 75)

print("\nInitializing RAG Agent...")

rag_agent = RAGAgent()

print("RAG Agent initialized successfully.")


# ============================================================
# TEST CASES
# ============================================================

test_cases = [
    {
        "name": "Annual Leave Policy",
        "question": "What is the annual leave policy?",
        "expected": [
            "full-time employees",
            "annual paid leave"
        ]
    },
    {
        "name": "Sick Leave Policy",
        "question": "What is the sick leave policy?",
        "expected": [
            "notify their manager",
            "medical documentation"
        ]
    },
    {
        "name": "Casual Leave Policy",
        "question": "What is the casual leave policy?",
        "expected": [
            "leave",
            "manager"
        ]
    },
    {
        "name": "Unsupported Office Location",
        "question": "What is the company's office location?",
        "expected": [
            "not provide enough verified information"
        ]
    }
]


# ============================================================
# RUN A SINGLE RAG QUERY
# ============================================================

def run_rag_query(question):
    """
    Run the question using whichever public method
    is available in the current RAGAgent implementation.
    """

    if hasattr(rag_agent, "run"):
        return rag_agent.run(question)

    if hasattr(rag_agent, "answer"):
        return rag_agent.answer(question)

    if hasattr(rag_agent, "process_query"):
        return rag_agent.process_query(question)

    raise AttributeError(
        "RAGAgent does not have run(), answer(), "
        "or process_query() method."
    )


# ============================================================
# EVALUATE ONE TEST CASE
# ============================================================

def evaluate_test_case(test_case):
    name = test_case["name"]
    question = test_case["question"]
    expected_terms = test_case["expected"]

    print("\n" + "-" * 75)
    print(f"TEST: {name}")
    print("-" * 75)

    print(f"Question: {question}")

    try:
        result = run_rag_query(question)

        if result is None:
            answer = ""
        else:
            answer = str(result)

        print(f"\nSystem Output:\n{answer}")

        answer_lower = answer.lower()

        missing_terms = []

        for term in expected_terms:
            if term.lower() not in answer_lower:
                missing_terms.append(term)

        if len(missing_terms) == 0:
            print("\nResult: PASS")
            return True

        print("\nResult: FAIL")
        print("Missing expected terms:", missing_terms)
        return False

    except Exception as error:
        print("\nResult: ERROR")
        print("Error:", error)
        return False


# ============================================================
# RUN ALL TESTS
# ============================================================

passed = 0
failed = 0

for test_case in test_cases:
    result = evaluate_test_case(test_case)

    if result:
        passed += 1
    else:
        failed += 1


# ============================================================
# FINAL SUMMARY
# ============================================================

total = passed + failed

if total > 0:
    accuracy = (passed / total) * 100
else:
    accuracy = 0


print("\n" + "=" * 75)
print("RAG EVALUATION SUMMARY")
print("=" * 75)

print(f"\nTotal Tests : {total}")
print(f"Passed      : {passed}")
print(f"Failed      : {failed}")
print(f"Accuracy    : {accuracy:.2f}%")

if failed == 0:
    print("\nOverall Result: ALL RAG TESTS PASSED")
else:
    print("\nOverall Result: SOME RAG TESTS FAILED")

print("=" * 75)

