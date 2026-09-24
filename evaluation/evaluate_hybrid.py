import os
import sys
import importlib.util


# ============================================================
# PATH SETUP
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

APP_PATH = os.path.join(
    PROJECT_ROOT,
    "app"
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

if APP_PATH not in sys.path:
    sys.path.insert(0, APP_PATH)


# ============================================================
# LOAD HYBRID COORDINATOR
# ============================================================

HYBRID_PATH = os.path.join(
    APP_PATH,
    "hybrid_coordinator.py"
)


spec = importlib.util.spec_from_file_location(
    "hybrid_coordinator",
    HYBRID_PATH
)

hybrid_module = importlib.util.module_from_spec(spec)

spec.loader.exec_module(hybrid_module)

HybridCoordinator = hybrid_module.HybridCoordinator


# ============================================================
# TEST CASES
# ============================================================

TEST_CASES = [

    {
        "name": "Employee Count",
        "question": "How many employees are there?",
        "expected": "100",
        "type": "SQL"
    },

    {
        "name": "Department Count",
        "question": "How many departments are there?",
        "expected": "6",
        "type": "SQL"
    },

    {
        "name": "Annual Leave",
        "question": "What is the annual leave policy?",
        "expected": "full-time employees",
        "type": "RAG"
    },

    {
        "name": "Sick Leave",
        "question": "What is the sick leave policy?",
        "expected": "notify their manager",
        "type": "RAG"
    },

    {
        "name": "Hybrid Query",
        "question":
            "How many employees are there and "
            "what is the annual leave policy?",
        "expected": [
            "100",
            "full-time employees"
        ],
        "type": "HYBRID"
    },

    {
        "name": "Unsupported Query",
        "question":
            "What is the company's office location?",
        "expected":
            "not provide enough verified information",
        "type": "UNSUPPORTED"
    }
]


# ============================================================
# CHECK RESULT
# ============================================================

def check_result(result, expected):

    result_text = str(result).lower()

    if isinstance(expected, list):

        for item in expected:

            if str(item).lower() not in result_text:
                return False

        return True

    return str(expected).lower() in result_text


# ============================================================
# MAIN EVALUATION
# ============================================================

def main():

    print("\n")
    print("=" * 75)
    print("ARES-RAG X — EVALUATION SUITE")
    print("=" * 75)

    print("\nInitializing Hybrid Coordinator...")

    coordinator = HybridCoordinator()


    total_tests = len(TEST_CASES)
    passed_tests = 0


    print("\n")
    print("=" * 75)
    print("RUNNING TESTS")
    print("=" * 75)


    for index, test in enumerate(TEST_CASES, start=1):

        print("\n")
        print("-" * 75)

        print(
            f"TEST {index}/{total_tests}"
        )

        print(
            f"Name: {test['name']}"
        )

        print(
            f"Type: {test['type']}"
        )

        print(
            f"Question: {test['question']}"
        )

        print(
            f"Expected: {test['expected']}"
        )

        print("-" * 75)


        try:

            result = coordinator.process_query(
                test["question"]
            )


            passed = check_result(
                result,
                test["expected"]
            )


            if passed:

                print("\nRESULT: PASS")

                passed_tests += 1

            else:

                print("\nRESULT: FAIL")


        except Exception as e:

            print("\nRESULT: ERROR")

            print(
                f"Error: {e}"
            )


    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    accuracy = (
        passed_tests / total_tests
    ) * 100


    print("\n")
    print("=" * 75)
    print("EVALUATION SUMMARY")
    print("=" * 75)

    print(
        f"\nTotal Tests : {total_tests}"
    )

    print(
        f"Passed      : {passed_tests}"
    )

    print(
        f"Failed      : {total_tests - passed_tests}"
    )

    print(
        f"Accuracy    : {accuracy:.2f}%"
    )


    print("\n")


    if accuracy == 100:

        print(
            "Overall Result: ALL TESTS PASSED"
        )

    elif accuracy >= 80:

        print(
            "Overall Result: MOST TESTS PASSED"
        )

    else:

        print(
            "Overall Result: IMPROVEMENT REQUIRED"
        )


    print("\n")
    print("=" * 75)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()
