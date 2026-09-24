from src.semantic_cache import SemanticCache


print("=" * 70)
print("TRUE SEMANTIC CACHE TEST")
print("=" * 70)


# Use a separate test cache
cache = SemanticCache(
    "data/semantic_test_cache.json",
    similarity_threshold=0.80
)


# Clear previous test data
cache.clear()


# ======================================================
# TEST 1 — STORE ORIGINAL QUESTION
# ======================================================

question_1 = "How many employees are there?"

answer_1 = "There are 100 employees."


print("\n")
print("=" * 70)
print("TEST 1 — STORE QUESTION")
print("=" * 70)

cache.set(
    question_1,
    answer_1
)

print("\nStored:")
print(question_1)

print("\nCache size:")
print(cache.size())


# ======================================================
# TEST 2 — SAME QUESTION
# ======================================================

print("\n")
print("=" * 70)
print("TEST 2 — EXACT SAME QUESTION")
print("=" * 70)

result = cache.get(
    "How many employees are there?"
)

print("\nResult:")

if result:

    print("CACHE HIT")
    print("Matched question:")
    print(result["question"])

    print("Similarity:")
    print(
        round(
            result["similarity"],
            4
        )
    )

    print("Answer:")
    print(result["answer"])

else:

    print("CACHE MISS")


# ======================================================
# TEST 3 — SIMILAR QUESTION
# ======================================================

print("\n")
print("=" * 70)
print("TEST 3 — SIMILAR QUESTION")
print("=" * 70)

similar_question = (
    "How many workers does the company have?"
)

print("\nNew question:")
print(similar_question)

result = cache.get(
    similar_question
)

print("\nResult:")

if result:

    print("CACHE HIT")
    print("Matched question:")
    print(result["question"])

    print("Similarity:")
    print(
        round(
            result["similarity"],
            4
        )
    )

    print("Answer:")
    print(result["answer"])

else:

    print("CACHE MISS")


# ======================================================
# TEST 4 — UNRELATED QUESTION
# ======================================================

print("\n")
print("=" * 70)
print("TEST 4 — UNRELATED QUESTION")
print("=" * 70)

unrelated_question = (
    "What is the company leave policy?"
)

print("\nNew question:")
print(unrelated_question)

result = cache.get(
    unrelated_question
)

print("\nResult:")

if result:

    print("CACHE HIT")
    print("Similarity:")
    print(
        round(
            result["similarity"],
            4
        )
    )

else:

    print("CACHE MISS")


# ======================================================
# COMPLETE
# ======================================================

print("\n")
print("=" * 70)
print("SEMANTIC CACHE TEST COMPLETED")
print("=" * 70)