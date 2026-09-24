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

from query_router import QueryRouter
from rag_agent import RAGAgent
from sql_agent import SQLAgent
from hybrid_agent import HybridAgent
from guardrails import Guardrails
from semantic_cache import SemanticCache


class AgentCoordinator:

    def __init__(self):

        self.router = QueryRouter()

        self.rag_agent = RAGAgent()
        self.sql_agent = SQLAgent()
        self.hybrid_agent = HybridAgent()

        self.guardrails = Guardrails()

        # ==================================================
        # SEMANTIC CACHE
        # ==================================================

        self.semantic_cache = SemanticCache()


    def run(self, query):

        # ==================================================
        # STEP 1 — QUERY GUARDRAILS
        # ==================================================

        validation = self.guardrails.validate_query(
            query
        )

        if not validation["allowed"]:

            return (
                "Request blocked by security guardrails. "
                + validation["reason"]
            )


        # ==================================================
        # STEP 2 — SEMANTIC CACHE
        # ==================================================

        cached_result = self.semantic_cache.get(
            query
        )

        print("\n" + "=" * 70)
        print("SEMANTIC CACHE")
        print("=" * 70)

        if cached_result:

            print("\nCACHE HIT")
            print("Returning cached answer.")

            return cached_result["answer"]

        else:

            print("\nCACHE MISS")
            print("Question not found in cache.")


        # ==================================================
        # STEP 3 — AGENT COORDINATOR
        # ==================================================

        print("\n" + "=" * 70)
        print("AGENT COORDINATOR")
        print("=" * 70)

        print("User Question:")
        print(query)


        # ==================================================
        # STEP 4 — ROUTING
        # ==================================================

        route = self.router.route(
            query
        )

        print("\nSelected Route:")
        print(route)


        # ==================================================
        # STEP 5 — SEND TO AGENT
        # ==================================================

        if route == "document":

            print(
                "\nSending query to RAG Agent..."
            )

            answer = self.rag_agent.run(
                query
            )

        elif route == "sql":

            print(
                "\nSending query to SQL Agent..."
            )

            answer = self.sql_agent.run(
                query
            )

        elif route == "hybrid":

            print(
                "\nSending query to Hybrid Agent..."
            )

            answer = self.hybrid_agent.run(
                query
            )

        else:

            answer = (
                "I could not determine which "
                "agent should handle this question."
            )


        # ==================================================
        # STEP 6 — ANSWER GUARDRAILS
        # ==================================================

        answer_validation = (
            self.guardrails.validate_answer(
                answer
            )
        )

        if not answer_validation["allowed"]:

            return (
                "The generated answer was blocked "
                "by security guardrails. "
                + answer_validation["reason"]
            )


        # ==================================================
        # STEP 7 — STORE ANSWER IN CACHE
        # ==================================================

        self.semantic_cache.set(
            query,
            answer
        )

        print("\n" + "=" * 70)
        print("SEMANTIC CACHE")
        print("=" * 70)

        print("\nCACHE STORED")
        print("Answer saved for future queries.")


        # ==================================================
        # STEP 8 — RETURN ANSWER
        # ==================================================

        return answer


# ==========================================================
# MAIN TEST
# ==========================================================

if __name__ == "__main__":

    coordinator = AgentCoordinator()

    question = input(
        "\nEnter your question: "
    )

    answer = coordinator.run(
        question
    )

    print("\n")
    print("=" * 70)
    print("FINAL COORDINATOR ANSWER")
    print("=" * 70)

    print(answer)