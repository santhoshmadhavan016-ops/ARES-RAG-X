import os
import json
import time
import sys


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(PROJECT_ROOT)
sys.path.append(
    os.path.join(PROJECT_ROOT, "src")
)


# ============================================================
# FILE PATHS
# ============================================================

TEST_FILE = os.path.join(
    PROJECT_ROOT,
    "evaluation",
    "test_questions.json"
)

REPORT_FILE = os.path.join(
    PROJECT_ROOT,
    "evaluation",
    "evaluation_report.json"
)

CACHE_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "semantic_cache.json"
)


# ============================================================
# CLEAR SEMANTIC CACHE
# ============================================================

print("\n" + "=" * 70)
print("PREPARING BASELINE EVALUATION")
print("=" * 70)

print("\nClearing semantic cache...")

try:

    os.makedirs(
        os.path.dirname(CACHE_FILE),
        exist_ok=True
    )

    with open(
        CACHE_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            [],
            file,
            indent=4
        )

    print("Semantic cache cleared successfully.")

except Exception as error:

    print(
        "Could not clear semantic cache:"
    )

    print(error)

    sys.exit(1)


# ============================================================
# IMPORT WORKFLOW
# ============================================================

try:

    from langgraph_workflow import build_workflow

except Exception as error:

    print("\nERROR IMPORTING WORKFLOW")
    print("-" * 70)
    print(error)

    sys.exit(1)


# ============================================================
# LOAD TEST QUESTIONS
# ============================================================

try:

    with open(
        TEST_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        test_questions = json.load(file)

except Exception as error:

    print("\nERROR LOADING TEST QUESTIONS")
    print("-" * 70)
    print(error)

    sys.exit(1)


# ============================================================
# BUILD WORKFLOW
# ============================================================

print("\nBuilding ARES-RAG X workflow...")

try:

    workflow = build_workflow()

except Exception as error:

    print("\nERROR BUILDING WORKFLOW")
    print("-" * 70)
    print(error)

    sys.exit(1)

print("Workflow ready.")


# ============================================================
# EVALUATION HEADER
# ============================================================

print("\n")
print("=" * 70)
print("ARES-RAG X EVALUATION SYSTEM")
print("=" * 70)

print("\nTotal Tests:")
print(len(test_questions))


# ============================================================
# EVALUATION VARIABLES
# ============================================================

total_tests = len(test_questions)

route_evaluated_tests = 0

route_passes = 0

answer_passes = 0

overall_passes = 0

cache_hits = 0

total_latency = 0.0

test_results = []


# ============================================================
# RUN TESTS
# ============================================================

for test in test_questions:

    test_id = test.get(
        "id",
        len(test_results) + 1
    )

    question = test.get(
        "question",
        ""
    )

    expected_route = test.get(
        "expected_route",
        ""
    ).lower().strip()

    expected_answer = test.get(
        "expected_answer_contains",
        ""
    ).lower().strip()


    # ========================================================
    # TEST HEADER
    # ========================================================

    print("\n")
    print("=" * 70)
    print(f"TEST {test_id}")
    print("=" * 70)

    print("\nQuestion:")
    print(question)

    print("\nExpected Route:")
    print(expected_route)


    # ========================================================
    # START TIMER
    # ========================================================

    start_time = time.perf_counter()


    # ========================================================
    # RUN WORKFLOW
    # ========================================================

    try:

        result = workflow.invoke(
            {
                "query": question,
                "route": "",
                "answer": "",
                "query_allowed": True,
                "answer_allowed": True,
                "guardrail_reason": "",
                "cache_hit": False
            }
        )

    except Exception as error:

        latency = (
            time.perf_counter()
            - start_time
        )

        total_latency += latency

        print("\nWORKFLOW ERROR")
        print("-" * 70)
        print(error)

        test_result = {

            "id": test_id,

            "question": question,

            "expected_route": expected_route,

            "actual_route": "",

            "expected_answer_contains": expected_answer,

            "actual_answer": "",

            "cache_hit": False,

            "route_test": "FAIL",

            "answer_test": "FAIL",

            "overall_test": "FAIL",

            "latency_seconds": round(
                latency,
                4
            ),

            "error": str(error)
        }

        test_results.append(
            test_result
        )

        continue


    # ========================================================
    # END TIMER
    # ========================================================

    latency = (
        time.perf_counter()
        - start_time
    )

    total_latency += latency


    # ========================================================
    # GET RESULT VALUES
    # ========================================================

    actual_route = result.get(
        "route",
        ""
    )

    actual_answer = result.get(
        "answer",
        ""
    )

    cache_hit = result.get(
        "cache_hit",
        False
    )

    query_allowed = result.get(
        "query_allowed",
        True
    )

    answer_allowed = result.get(
        "answer_allowed",
        True
    )


    # ========================================================
    # NORMALIZE VALUES
    # ========================================================

    if actual_route is None:
        actual_route = ""

    actual_route = str(
        actual_route
    ).lower().strip()


    if actual_answer is None:
        actual_answer = ""

    actual_answer = str(
        actual_answer
    ).strip()


    cache_hit = bool(
        cache_hit
    )


    # ========================================================
    # CACHE STATISTICS
    # ========================================================

    if cache_hit:

        cache_hits += 1


    # ========================================================
    # PRINT BASIC RESULT
    # ========================================================

    print("\nCache Hit:")
    print(cache_hit)

    if cache_hit:

        print("\nActual Route:")
        print(
            "(Router bypassed because of cache hit)"
        )

    else:

        print("\nActual Route:")
        print(actual_route)


    # ========================================================
    # ANSWER EXPECTATION
    # ========================================================

    print("\nExpected Answer Contains:")
    print(expected_answer)

    print("\nActual Answer:")
    print(actual_answer)


    # ========================================================
    # ROUTE EVALUATION
    # ========================================================
    #
    # Cache hits intentionally bypass the router.
    #
    # Therefore:
    #
    # CACHE HIT
    #     ↓
    # Router was not executed
    #     ↓
    # Route cannot be evaluated
    #
    # We exclude cache-hit tests from route accuracy.
    #
    # ========================================================

    if cache_hit:

        route_evaluation = (
            "SKIPPED — CACHE HIT"
        )

        route_passed = True

    else:

        route_evaluated_tests += 1

        if actual_route == expected_route:

            route_passed = True

            route_passes += 1

            route_evaluation = "PASS"

        else:

            route_passed = False

            route_evaluation = "FAIL"


    # ========================================================
    # ANSWER EVALUATION
    # ========================================================

    if not expected_answer:

        answer_passed = True

    else:

        answer_passed = (
            expected_answer
            in actual_answer.lower()
        )


    if answer_passed:

        answer_passes += 1

        answer_evaluation = "PASS"

    else:

        answer_evaluation = "FAIL"


    # ========================================================
    # OVERALL EVALUATION
    # ========================================================

    if (
        route_passed
        and answer_passed
        and query_allowed
        and answer_allowed
    ):

        overall_passed = True

        overall_passes += 1

        overall_evaluation = "PASS"

    else:

        overall_passed = False

        overall_evaluation = "FAIL"


    # ========================================================
    # PRINT EVALUATION
    # ========================================================

    print("\nLatency:")
    print(
        f"{latency:.4f} seconds"
    )

    print("\nRoute Test:")
    print(route_evaluation)

    print("\nAnswer Test:")
    print(answer_evaluation)

    print("\nOverall Test:")
    print(overall_evaluation)


    # ========================================================
    # STORE RESULT
    # ========================================================

    test_result = {

        "id": test_id,

        "question": question,

        "expected_route": expected_route,

        "actual_route": (
            actual_route
            if not cache_hit
            else ""
        ),

        "expected_answer_contains": (
            expected_answer
        ),

        "actual_answer": actual_answer,

        "cache_hit": cache_hit,

        "query_allowed": query_allowed,

        "answer_allowed": answer_allowed,

        "route_test": route_evaluation,

        "answer_test": answer_evaluation,

        "overall_test": overall_evaluation,

        "latency_seconds": round(
            latency,
            4
        )
    }

    test_results.append(
        test_result
    )


# ============================================================
# CALCULATE METRICS
# ============================================================

if route_evaluated_tests > 0:

    route_accuracy = (
        route_passes
        / route_evaluated_tests
        * 100
    )

else:

    route_accuracy = 0.0


if total_tests > 0:

    answer_accuracy = (
        answer_passes
        / total_tests
        * 100
    )

    overall_accuracy = (
        overall_passes
        / total_tests
        * 100
    )

    cache_hit_rate = (
        cache_hits
        / total_tests
        * 100
    )

    average_latency = (
        total_latency
        / total_tests
    )

else:

    answer_accuracy = 0.0

    overall_accuracy = 0.0

    cache_hit_rate = 0.0

    average_latency = 0.0


# ============================================================
# EVALUATION SUMMARY
# ============================================================

print("\n")
print("=" * 70)
print("ARES-RAG X EVALUATION SUMMARY")
print("=" * 70)

print(
    f"\nTotal Tests: {total_tests}"
)

print(
    f"Route-Evaluated Tests: "
    f"{route_evaluated_tests}"
)

print(
    f"Route Accuracy: "
    f"{route_accuracy:.2f}%"
)

print(
    f"Answer Accuracy: "
    f"{answer_accuracy:.2f}%"
)

print(
    f"Overall Accuracy: "
    f"{overall_accuracy:.2f}%"
)

print(
    f"Cache Hit Rate: "
    f"{cache_hit_rate:.2f}%"
)

print(
    f"Average Latency: "
    f"{average_latency:.4f} seconds"
)

print(
    f"\nPassed Tests: "
    f"{overall_passes}/{total_tests}"
)


# ============================================================
# CREATE EVALUATION REPORT
# ============================================================

evaluation_report = {

    "project": "ARES-RAG X",

    "evaluation_type": (
        "Baseline Evaluation"
    ),

    "total_tests": total_tests,

    "route_evaluated_tests": (
        route_evaluated_tests
    ),

    "route_accuracy_percent": round(
        route_accuracy,
        2
    ),

    "answer_accuracy_percent": round(
        answer_accuracy,
        2
    ),

    "overall_accuracy_percent": round(
        overall_accuracy,
        2
    ),

    "cache_hit_rate_percent": round(
        cache_hit_rate,
        2
    ),

    "average_latency_seconds": round(
        average_latency,
        4
    ),

    "passed_tests": overall_passes,

    "failed_tests": (
        total_tests
        - overall_passes
    ),

    "tests": test_results
}


# ============================================================
# SAVE REPORT
# ============================================================

try:

    with open(
        REPORT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            evaluation_report,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\n")
    print("Evaluation report saved to:")

    print(
        REPORT_FILE
    )

except Exception as error:

    print("\nERROR SAVING REPORT")
    print("-" * 70)
    print(error)


# ============================================================
# COMPLETION
# ============================================================

print("\n")
print("=" * 70)
print("EVALUATION COMPLETED")
print("=" * 70)
