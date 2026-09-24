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
from conversation_memory import ConversationMemory


class AgentCoordinator:

    def __init__(self):

        self.router = QueryRouter()

        self.rag_agent = RAGAgent()

        self.sql_agent = SQLAgent()

        self.hybrid_agent = HybridAgent()

        self.guardrails = Guardrails()

        self.memory = ConversationMemory()


    def run(self, query):

        print("\n" + "=" * 70)
        print("AGENT COORDINATOR")
        print("=" * 70)

        print("User Question:")
        print(query)


        # --------------------------------------------------
        # 1. SECURITY CHECK
        # --------------------------------------------------

        validation = self.guardrails.validate_query(query)

        if not validation["allowed"]:

            return (
                "Request blocked by security guardrails. "
                + validation["reason"]
            )


        # --------------------------------------------------
        # 2. SELECT ROUTE
        # --------------------------------------------------

        route = self.router.route(query)

        print("\nSelected Route:")
        print(route)


        # --------------------------------------------------
        # 3. SEND TO APPROPRIATE AGENT
        # --------------------------------------------------

        if route == "document":

            print("\nSending query to RAG Agent...")

            answer = self.rag_agent.run(query)


        elif route == "sql":

            print("\nSending query to SQL Agent...")

            answer = self.sql_agent.run(query)


        elif route == "hybrid":

            print("\nSending query to Hybrid Agent...")

            answer = self.hybrid_agent.run(query)


        else:

            answer = (
                "I could not determine which "
                "agent should handle this question."
            )


        # --------------------------------------------------
        # 4. ANSWER SECURITY CHECK
        # --------------------------------------------------

        answer_validation = self.guardrails.validate_answer(answer)

        if not answer_validation["allowed"]:

            return (
                "The generated answer was blocked "
                "by security guardrails. "
                + answer_validation["reason"]
            )


        # --------------------------------------------------
        # 5. SAVE CONVERSATION
        # --------------------------------------------------

        self.memory.add_message(
            "user",
            query
        )

        self.memory.add_message(
            "assistant",
            answer
        )


        return answer


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    coordinator = AgentCoordinator()

    while True:

        question = input("\nEnter your question: ")

        if question.lower().strip() in ["exit", "quit"]:
            break

        answer = coordinator.run(question)

        print("\n")
        print("=" * 70)
        print("FINAL COORDINATOR ANSWER")
        print("=" * 70)

        print(answer)

        print("\n")
        print("=" * 70)
        print("CONVERSATION MEMORY")
        print("=" * 70)

        print(coordinator.memory.get_history())


    
