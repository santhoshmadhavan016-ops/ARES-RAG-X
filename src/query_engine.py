import sys
import os

# ======================================================
# ADD SRC FOLDER TO PYTHON PATH
# ======================================================

sys.path.append(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

# ======================================================
# IMPORT PROJECT COMPONENTS
# ======================================================

from query_router import QueryRouter
from retriever import retrieve_and_rerank
from text2sql import Text2SQL
from answer_generator import AnswerGenerator
from guardrails import Guardrails
from semantic_cache import SemanticCache


# ======================================================
# QUERY ENGINE
# ======================================================

class QueryEngine:

    def __init__(self):

        # Query Router
        self.router = QueryRouter()

        # Text-to-SQL system
        self.text2sql = Text2SQL()

        # LLM Answer Generator
        self.answer_generator = AnswerGenerator()

        # Security Guardrails
        self.guardrails = Guardrails()

        # Semantic Cache
        self.semantic_cache = SemanticCache()


    # ==================================================
    # MAIN QUERY FUNCTION
    # ==================================================

    def answer_query(self, query):

        # ==================================================
        # 1. QUERY GUARDRAIL
        # ==================================================

        validation = self.guardrails.validate_query(query)

        if not validation["allowed"]:

            return (
                "Request blocked by security guardrails. "
                + validation["reason"]
            )


        # ==================================================
        # 2. SEMANTIC CACHE CHECK
        # ==================================================

        cached_result = self.semantic_cache.get(query)

        if cached_result:

            print("\n" + "=" * 70)
            print("SEMANTIC CACHE")
            print("=" * 70)

            print("\nCACHE HIT")
            print("Returning previously generated answer.")

            return cached_result["answer"]


        print("\n" + "=" * 70)
        print("SEMANTIC CACHE")
        print("=" * 70)

        print("\nCACHE MISS")
        print("Processing question through the AI pipeline...")


        # ==================================================
        # 3. QUERY ROUTER
        # ==================================================

        route = self.router.route(query)

        print("\n" + "=" * 70)
        print("QUERY")
        print("=" * 70)

        print(query)

        print("\nSELECTED ROUTE:")
        print(route)


        # ==================================================
        # 4. SQL ROUTE
        # ==================================================

        if route == "sql":

            print("\n")
            print("=" * 70)
            print("SQL AGENT")
            print("=" * 70)

            try:

                # Generate SQL
                sql = self.text2sql.generate_sql(query)

                print("\nGENERATED SQL:")
                print(sql)


                # Execute SQL
                sql_result = self.text2sql.execute_query(sql)

                print("\nSQL RESULT:")
                print(sql_result)


                # Generate natural language answer
                answer = self.answer_generator.generate_sql_answer(
                    query,
                    sql_result
                )

            except Exception as e:

                print("\nSQL ERROR:")
                print(e)

                answer = (
                    "I could not retrieve the required "
                    "information from the database."
                )


        # ==================================================
        # 5. DOCUMENT / RAG ROUTE
        # ==================================================

        elif route == "document":

            print("\n")
            print("=" * 70)
            print("RAG AGENT")
            print("=" * 70)

            try:

                # Retrieve documents
                rag_results = retrieve_and_rerank(
                    query,
                    top_k=3
                )

                print("\nRETRIEVED DOCUMENTS:")
                print(len(rag_results))


                # Generate answer from documents
                answer = self.answer_generator.generate_document_answer(
                    query,
                    rag_results
                )

            except Exception as e:

                print("\nRAG ERROR:")
                print(e)

                answer = (
                    "I could not retrieve the required "
                    "information from the company documents."
                )


        # ==================================================
        # 6. HYBRID ROUTE
        # ==================================================

        elif route == "hybrid":

            print("\n")
            print("=" * 70)
            print("HYBRID AGENT")
            print("=" * 70)


            # --------------------------------------------------
            # PART A — RAG
            # --------------------------------------------------

            print("\n[1] RETRIEVING DOCUMENT INFORMATION...")

            rag_results = []

            try:

                rag_results = retrieve_and_rerank(
                    query,
                    top_k=3
                )

                print(
                    "Retrieved documents:",
                    len(rag_results)
                )

            except Exception as e:

                print("\nRAG ERROR:")
                print(e)


            # --------------------------------------------------
            # PART B — SQL
            # --------------------------------------------------

            print("\n[2] GENERATING DATABASE QUERY...")

            sql = None
            sql_result = None

            try:

                sql = self.text2sql.generate_sql(query)

                print("\nGENERATED SQL:")
                print(sql)


                if sql:

                    print("\n[3] EXECUTING DATABASE QUERY...")

                    sql_result = self.text2sql.execute_query(
                        sql
                    )

                    print("\nSQL RESULT:")
                    print(sql_result)

                else:

                    print(
                        "\nNo SQL query was generated."
                    )

            except Exception as e:

                print("\nSQL ERROR:")
                print(e)


            # --------------------------------------------------
            # PART C — COORDINATOR
            # --------------------------------------------------

            print("\n")
            print("=" * 70)
            print("HYBRID COORDINATOR")
            print("=" * 70)

            try:

                answer = self.answer_generator.generate_hybrid_answer(
                    query,
                    sql_result,
                    rag_results
                )

            except Exception as e:

                print("\nCOORDINATOR ERROR:")
                print(e)

                answer = (
                    "I could not combine the information "
                    "from the company documents and database."
                )


        # ==================================================
        # 7. UNKNOWN ROUTE
        # ==================================================

        else:

            answer = (
                "I could not determine how to answer "
                "this question."
            )


        # ==================================================
        # 8. ANSWER GUARDRAIL
        # ==================================================

        answer_validation = self.guardrails.validate_answer(
            answer
        )

        if not answer_validation["allowed"]:

            return (
                "The generated answer was blocked by "
                "security guardrails. "
                + answer_validation["reason"]
            )


        # ==================================================
        # 9. STORE ANSWER IN SEMANTIC CACHE
        # ==================================================

        self.semantic_cache.set(
            query,
            answer
        )

        print("\n")
        print("=" * 70)
        print("SEMANTIC CACHE")
        print("=" * 70)

        print("\nCACHE STORED")
        print("Answer has been saved for future queries.")


        # ==================================================
        # 10. RETURN FINAL ANSWER
        # ==================================================

        return answer


# ======================================================
# INTERACTIVE MODE
# ======================================================

if __name__ == "__main__":

    engine = QueryEngine()

    print("\n")
    print("=" * 70)
    print("ARES-RAG X QUERY ENGINE")
    print("=" * 70)

    print("\nType 'exit' or 'quit' to stop.")

    while True:

        query = input(
            "\nEnter your question: "
        )


        # --------------------------------------------------
        # EXIT
        # --------------------------------------------------

        if query.lower().strip() in [
            "exit",
            "quit"
        ]:

            print("\nExiting ARES-RAG X.")

            break


        # --------------------------------------------------
        # EMPTY QUESTION
        # --------------------------------------------------

        if not query.strip():

            print(
                "\nPlease enter a question."
            )

            continue


        # --------------------------------------------------
        # PROCESS QUESTION
        # --------------------------------------------------

        answer = engine.answer_query(
            query
        )


        # --------------------------------------------------
        # FINAL ANSWER
        # --------------------------------------------------

        print("\n")
        print("=" * 70)
        print("FINAL ANSWER")
        print("=" * 70)

        print(answer)
        