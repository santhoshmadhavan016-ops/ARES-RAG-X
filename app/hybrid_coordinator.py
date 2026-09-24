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

SRC_PATH = os.path.join(
    PROJECT_ROOT,
    "src"
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

if APP_PATH not in sys.path:
    sys.path.insert(0, APP_PATH)

if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)


# ============================================================
# MODULE LOADER
# ============================================================

def load_module(module_name, file_path):

    spec = importlib.util.spec_from_file_location(
        module_name,
        file_path
    )

    module = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(module)

    return module


# ============================================================
# LOAD SQL AGENT
# ============================================================

sql_agent_path = os.path.join(
    APP_PATH,
    "sql_agent.py"
)

sql_module = load_module(
    "sql_agent_module",
    sql_agent_path
)

SQLAgent = sql_module.SQLAgent


# ============================================================
# LOAD RAG AGENT
# ============================================================

rag_agent_path = os.path.join(
    APP_PATH,
    "rag_agent.py"
)

rag_module = load_module(
    "rag_agent_module",
    rag_agent_path
)

RAGAgent = rag_module.RAGAgent


# ============================================================
# HYBRID COORDINATOR
# ============================================================

class HybridCoordinator:

    def __init__(self):

        print("\n")
        print("=" * 70)
        print("ARES-RAG X — HYBRID COORDINATOR")
        print("=" * 70)

        print("\nInitializing SQL Agent...")

        self.sql_agent = SQLAgent()

        print("\nInitializing RAG Agent...")

        self.rag_agent = RAGAgent()

        print("\nHybrid Coordinator initialized successfully.")


    # ========================================================
    # QUESTION DECOMPOSITION
    # ========================================================

    def decompose_question(self, question):

        question_lower = question.lower()

        sql_question = None
        rag_question = None


        # ====================================================
        # SQL QUESTIONS
        # ====================================================

        if (
            "how many employees" in question_lower
            or "number of employees" in question_lower
            or "total employees" in question_lower
            or "employee count" in question_lower
        ):

            sql_question = "How many employees are there?"


        elif (
            "how many departments" in question_lower
            or "number of departments" in question_lower
            or "total departments" in question_lower
            or "department count" in question_lower
        ):

            sql_question = "How many departments are there?"


        elif (
            "how many customers" in question_lower
            or "number of customers" in question_lower
            or "total customers" in question_lower
            or "customer count" in question_lower
        ):

            sql_question = "How many customers are there?"


        elif (
            "how many projects" in question_lower
            or "number of projects" in question_lower
            or "total projects" in question_lower
            or "project count" in question_lower
        ):

            sql_question = "How many projects are there?"


        # ====================================================
        # RAG QUESTIONS
        # ====================================================

        if (
            "annual leave" in question_lower
            or "annual leave policy" in question_lower
        ):

            rag_question = "What is the annual leave policy?"


        elif (
            "sick leave" in question_lower
            or "sick leave policy" in question_lower
        ):

            rag_question = "What is the sick leave policy?"


        elif (
            "casual leave" in question_lower
            or "casual leave policy" in question_lower
        ):

            rag_question = "What is the casual leave policy?"


        elif (
            "leave policy" in question_lower
            or "leave rules" in question_lower
        ):

            rag_question = "What is the leave policy?"


        # ====================================================
        # FALLBACK ROUTE
        # ====================================================

        # If the question does not match any known SQL/RAG
        # pattern, send it to RAG.
        #
        # RAG will then search the enterprise documents.
        #
        # If the information does not exist in the documents,
        # the RAG pipeline should reject/limit the answer.
        # ====================================================

        if sql_question is None and rag_question is None:

            rag_question = question

        return sql_question, rag_question


    # ========================================================
    # RUN SQL AGENT
    # ========================================================

    def run_sql(self, question):

        print("\n")
        print("=" * 70)
        print("HYBRID → SQL AGENT")
        print("=" * 70)

        print("\nSQL Question:")
        print(question)

        try:

            if hasattr(self.sql_agent, "run"):

                result = self.sql_agent.run(
                    question
                )

            elif hasattr(self.sql_agent, "answer"):

                result = self.sql_agent.answer(
                    question
                )

            elif hasattr(self.sql_agent, "process_query"):

                result = self.sql_agent.process_query(
                    question
                )

            else:

                raise AttributeError(
                    "SQLAgent does not have "
                    "run(), answer(), or process_query()"
                )

            return result

        except Exception as e:

            print("\nSQL Agent Error:")
            print(e)

            return f"SQL Agent Error: {e}"


    # ========================================================
    # RUN RAG AGENT
    # ========================================================

    def run_rag(self, question):

        print("\n")
        print("=" * 70)
        print("HYBRID → RAG AGENT")
        print("=" * 70)

        print("\nRAG Question:")
        print(question)

        try:

            if hasattr(self.rag_agent, "run"):

                result = self.rag_agent.run(
                    question
                )

            elif hasattr(self.rag_agent, "answer"):

                result = self.rag_agent.answer(
                    question
                )

            elif hasattr(self.rag_agent, "process_query"):

                result = self.rag_agent.process_query(
                    question
                )

            else:

                raise AttributeError(
                    "RAGAgent does not have "
                    "run(), answer(), or process_query()"
                )

            return result

        except Exception as e:

            print("\nRAG Agent Error:")
            print(e)

            return f"RAG Agent Error: {e}"


    # ========================================================
    # COMBINE RESULTS
    # ========================================================

    def combine_results(
        self,
        original_question,
        sql_question=None,
        rag_question=None,
        sql_result=None,
        rag_result=None
    ):

        print("\n")
        print("=" * 70)
        print("COMBINING RESULTS")
        print("=" * 70)


        # ====================================================
        # SQL + RAG
        # ====================================================

        if (
            sql_result is not None
            and rag_result is not None
        ):

            final_answer = (
                "Based on the company data "
                "and policy documents:\n"
            )

            final_answer += (
                "\nEmployee / Company Data:\n"
            )

            final_answer += str(
                sql_result
            )

            final_answer += (
                "\n\nPolicy / Document Information:\n"
            )

            final_answer += str(
                rag_result
            )

            return final_answer


        # ====================================================
        # SQL ONLY
        # ====================================================

        if sql_result is not None:

            final_answer = (
                "Based on the company data:\n\n"
            )

            final_answer += str(
                sql_result
            )

            return final_answer


        # ====================================================
        # RAG ONLY
        # ====================================================

        if rag_result is not None:

            final_answer = (
                "Based on the enterprise documents:\n\n"
            )

            final_answer += str(
                rag_result
            )

            return final_answer


        # ====================================================
        # NOTHING
        # ====================================================

        return (
            "I could not find sufficient information "
            "to answer this question."
        )


    # ========================================================
    # PROCESS QUERY
    # ========================================================

    def process_query(self, question):

        print("\n")
        print("=" * 70)
        print("HYBRID QUERY")
        print("=" * 70)

        print("\nUser Question:")
        print(question)


        # ====================================================
        # DECOMPOSE
        # ====================================================

        sql_question, rag_question = (
            self.decompose_question(
                question
            )
        )


        print("\n")
        print("=" * 70)
        print("QUESTION DECOMPOSITION")
        print("=" * 70)


        print("\nSQL Question:")

        if sql_question:

            print(sql_question)

        else:

            print("None")


        print("\nRAG Question:")

        if rag_question:

            print(rag_question)

        else:

            print("None")


        sql_result = None
        rag_result = None


        # ====================================================
        # RUN SQL
        # ====================================================

        if sql_question:

            sql_result = self.run_sql(
                sql_question
            )

            print("\nSQL Result:")
            print(sql_result)


        # ====================================================
        # RUN RAG
        # ====================================================

        if rag_question:

            rag_result = self.run_rag(
                rag_question
            )

            print("\nRAG Result:")
            print(rag_result)


        # ====================================================
        # COMBINE
        # ====================================================

        final_answer = self.combine_results(
            original_question=question,
            sql_question=sql_question,
            rag_question=rag_question,
            sql_result=sql_result,
            rag_result=rag_result
        )


        # ====================================================
        # FINAL ANSWER
        # ====================================================

        print("\n")
        print("=" * 70)
        print("FINAL HYBRID ANSWER")
        print("=" * 70)

        print(final_answer)

        print("\n")

        return final_answer


# ============================================================
# INTERACTIVE TESTING
# ============================================================

if __name__ == "__main__":

    coordinator = HybridCoordinator()


    print("\n")
    print("=" * 70)
    print("ARES-RAG X INTERACTIVE TEST")
    print("=" * 70)

    print("\nYou can now test different questions.")

    print("\nRecommended tests:")

    print(
        "1. How many employees are there?"
    )

    print(
        "2. What is the annual leave policy?"
    )

    print(
        "3. How many employees are there "
        "and what is the annual leave policy?"
    )

    print(
        "4. How many departments are there?"
    )

    print(
        "5. What is the sick leave policy?"
    )

    print(
        "6. What is the casual leave policy?"
    )

    print(
        "7. What is the company's office location?"
    )

    print("\nType 'exit' to stop.")


    # ========================================================
    # INPUT LOOP
    # ========================================================

    while True:

        question = input(
            "\nEnter your question: "
        )


        # ----------------------------------------------------
        # EXIT
        # ----------------------------------------------------

        if question.lower().strip() == "exit":

            print(
                "\nExiting ARES-RAG X..."
            )

            break


        # ----------------------------------------------------
        # EMPTY INPUT
        # ----------------------------------------------------

        if not question.strip():

            print(
                "\nPlease enter a question."
            )

            continue


        # ----------------------------------------------------
        # PROCESS
        # ----------------------------------------------------

        try:

            coordinator.process_query(
                question
            )

        except Exception as e:

            print("\n")
            print("=" * 70)
            print("ERROR")
            print("=" * 70)

            print(e)
