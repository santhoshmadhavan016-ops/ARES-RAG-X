import sys
import os

# Add project root
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(PROJECT_ROOT)
sys.path.append(
    os.path.join(PROJECT_ROOT, "src")
)

from retriever import retrieve_and_rerank
from text2sql import Text2SQL
from answer_generator import AnswerGenerator


class HybridAgent:

    def __init__(self):

        self.text2sql = Text2SQL()
        self.answer_generator = AnswerGenerator()

    def run(self, query):

        print("\n" + "=" * 70)
        print("HYBRID AGENT")
        print("=" * 70)

        print("Question:")
        print(query)

        # --------------------------------------------------
        # STEP 1: Retrieve company documents
        # --------------------------------------------------

        rag_results = retrieve_and_rerank(
            query,
            top_k=3
        )

        print("\nRAG Results:")
        print(len(rag_results))

        # --------------------------------------------------
        # STEP 2: Generate SQL
        # --------------------------------------------------

        sql = self.text2sql.generate_sql(query)

        print("\nGenerated SQL:")
        print(sql)

        # --------------------------------------------------
        # STEP 3: Execute SQL
        # --------------------------------------------------

        sql_result = None

        if sql:
            sql_result = self.text2sql.execute_query(
                sql
            )

        # --------------------------------------------------
        # STEP 4: Combine SQL + RAG
        # --------------------------------------------------

        answer = self.answer_generator.generate_hybrid_answer(
            query,
            sql_result,
            rag_results
        )

        return answer


# ==========================================================
# TEST HYBRID AGENT
# ==========================================================

if __name__ == "__main__":

    agent = HybridAgent()

    question = input(
        "\nEnter a hybrid question: "
    )

    answer = agent.run(question)

    print("\n")
    print("=" * 70)
    print("HYBRID AGENT ANSWER")
    print("=" * 70)

    print(answer)