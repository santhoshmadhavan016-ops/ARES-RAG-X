import sys
import os

# ==========================================================
# PROJECT ROOT
# ==========================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(PROJECT_ROOT)

sys.path.append(
    os.path.join(PROJECT_ROOT, "src")
)


# ==========================================================
# IMPORTS
# ==========================================================

from retriever import retrieve_and_rerank
from answer_generator import AnswerGenerator
from self_rag import SelfRAG


# ==========================================================
# RAG AGENT
# ==========================================================

class RAGAgent:

    def __init__(self):

        self.answer_generator = AnswerGenerator()

        self.self_rag = SelfRAG()


    def run(self, query):

        print("\n")
        print("=" * 70)
        print("RAG AGENT")
        print("=" * 70)

        print("\nUser Question:")
        print(query)


        # ==================================================
        # RETRIEVAL
        # ==================================================

        print("\n")
        print("=" * 70)
        print("RAG AGENT — RETRIEVAL")
        print("=" * 70)

        rag_results = retrieve_and_rerank(
            query,
            top_k=5
        )


        if not rag_results:

            return (
                "The information was not found "
                "in the company documents."
            )


        # ==================================================
        # EXTRACT DOCUMENTS
        # ==================================================

        documents = []

        for result in rag_results:

            documents.append(
                result["document"]
            )


        # ==================================================
        # ANSWER GENERATION
        # ==================================================

        print("\n")
        print("=" * 70)
        print("RAG AGENT — ANSWER GENERATION")
        print("=" * 70)

        answer = (
            self.answer_generator.generate_document_answer(
                query,
                rag_results
            )
        )


        print("\nGenerated Answer:")
        print("-" * 70)
        print(answer)


        # ==================================================
        # SELF-RAG VERIFICATION
        # ==================================================

        print("\n")
        print("=" * 70)
        print("SELF-RAG VERIFICATION")
        print("=" * 70)

        verification = (
            self.self_rag.evaluate_answer(
                query,
                answer,
                documents
            )
        )


        print("\nSelf-RAG Result:")
        print(
            verification["supported"]
        )


        print("\nReason:")
        print(
            verification["reason"]
        )


        # ==================================================
        # SELF-RAG PASSED
        # ==================================================

        if verification["supported"]:

            print("\n")
            print("=" * 70)
            print("SELF-RAG PASSED")
            print("=" * 70)

            print(
                "\nGenerated answer is "
                "supported by the documents."
            )

            return answer


        # ==================================================
        # SELF-RAG FAILED
        # ==================================================

        print("\n")
        print("=" * 70)
        print("SELF-RAG FAILED")
        print("=" * 70)

        print(
            "\nGenerated answer contains "
            "unsupported information."
        )


        # ==================================================
        # REGENERATE
        # ==================================================

        print(
            "\nRegenerating answer using "
            "enterprise documents..."
        )


        regenerated_answer = (
            self.self_rag.regenerate_answer(
                query,
                documents
            )
        )


        print("\nRegenerated Answer:")
        print("-" * 70)
        print(regenerated_answer)


        # ==================================================
        # SECOND VERIFICATION
        # ==================================================

        print("\n")
        print("=" * 70)
        print("SELF-RAG SECOND VERIFICATION")
        print("=" * 70)


        second_verification = (
            self.self_rag.evaluate_answer(
                query,
                regenerated_answer,
                documents
            )
        )


        print("\nSecond Self-RAG Result:")

        print(
            second_verification[
                "supported"
            ]
        )


        print("\nReason:")

        print(
            second_verification[
                "reason"
            ]
        )


        # ==================================================
        # REGENERATION PASSED
        # ==================================================

        if second_verification[
            "supported"
        ]:

            print("\n")
            print("=" * 70)
            print("SELF-RAG REGENERATION PASSED")
            print("=" * 70)

            return regenerated_answer


        # ==================================================
        # FALLBACK
        # ==================================================

        print("\n")
        print("=" * 70)
        print("SELF-RAG FALLBACK")
        print("=" * 70)


        return (
            "The available enterprise documents "
            "do not provide enough verified "
            "information to answer this question "
            "reliably."
        )


# ==========================================================
# TEST RAG AGENT
# ==========================================================

if __name__ == "__main__":

    agent = RAGAgent()

    query = (
        "What are the rules for remote access?"
    )

    print("\n")
    print("=" * 70)
    print("RAG AGENT + SELF-RAG TEST")
    print("=" * 70)

    final_answer = agent.run(
        query
    )

    print("\n")
    print("=" * 70)
    print("FINAL ANSWER")
    print("=" * 70)

    print("\n")
    print(final_answer)
    