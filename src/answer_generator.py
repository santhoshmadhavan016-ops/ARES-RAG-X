from llm import LLM


class AnswerGenerator:

    def __init__(self):

        self.llm = LLM()


    # ======================================================
    # FORMAT SQL RESULT
    # ======================================================

    def format_sql_result(self, sql_result):

        if sql_result is None:
            return ""

        if "error" in sql_result:

            return (
                f"Database error: "
                f"{sql_result['error']}"
            )

        columns = sql_result.get(
            "columns",
            []
        )

        rows = sql_result.get(
            "results",
            []
        )

        if not rows:

            return "No records were found."

        formatted_rows = []

        for index, row in enumerate(
            rows,
            start=1
        ):

            row_data = []

            for column, value in zip(
                columns,
                row
            ):

                row_data.append(
                    f"{column}: {value}"
                )

            formatted_rows.append(
                f"{index}. "
                + ", ".join(row_data)
            )

        return "\n".join(
            formatted_rows
        )


    # ======================================================
    # SQL ANSWER
    # ======================================================

    def generate_sql_answer(
        self,
        query,
        sql_result
    ):

        if sql_result is None:

            return (
                "I could not generate an "
                "SQL query for this question."
            )

        if "error" in sql_result:

            return (
                "Sorry, I could not retrieve "
                "the data. "
                f"Error: {sql_result['error']}"
            )

        formatted_result = (
            self.format_sql_result(
                sql_result
            )
        )

        prompt = f"""
You are an enterprise AI assistant
for Nova Corp.

Answer the user's question using ONLY
the database result provided below.

USER QUESTION:
{query}

DATABASE RESULT:
{formatted_result}

RULES:

1. Give a clear and simple answer.

2. Use ONLY the database result.

3. Do not invent information.

4. Preserve all important numbers exactly.

5. If the result contains a count,
   report the exact count.

6. If the result contains multiple records,
   do not change or invent the records.

7. Do not add information that is not
   present in the database result.

8. Do not say information is missing if
   the database result directly answers
   the question.

Return only the final answer.
"""

        return self.llm.generate(
            prompt
        ).strip()


    # ======================================================
    # DOCUMENT / RAG ANSWER
    # ======================================================

    def generate_document_answer(
        self,
        query,
        rag_results
    ):

        if not rag_results:

            return (
                "The information was not found "
                "in the company documents."
            )

        # --------------------------------------------------
        # HIGHEST-RANKED RESULT
        # --------------------------------------------------

        best_result = rag_results[0]

        best_title = (
            best_result["metadata"].get(
                "title",
                "Company Document"
            )
        )

        best_document = (
            best_result["document"]
        )

        # --------------------------------------------------
        # BUILD DOCUMENT CONTEXT
        # --------------------------------------------------

        context = ""

        for index, item in enumerate(
            rag_results,
            start=1
        ):

            title = (
                item["metadata"].get(
                    "title",
                    "Company Document"
                )
            )

            document = item["document"]

            context += f"""
Retrieved Result {index}

Title:
{title}

Content:
{document}

"""

        # --------------------------------------------------
        # DOCUMENT PROMPT
        # --------------------------------------------------

        prompt = f"""
You are an enterprise AI assistant
for Nova Corp.

Answer the user's question using ONLY
the retrieved company documents.

USER QUESTION:
{query}

HIGHEST-RANKED RESULT:

Title:
{best_title}

Content:
{best_document}

ADDITIONAL RETRIEVED CONTEXT:
{context}

RULES:

1. The highest-ranked result is the
   primary source.

2. If the highest-ranked result directly
   answers the question, use it.

3. Use additional results only when
   relevant.

4. Do not invent information.

5. Do not use outside knowledge.

6. Do not contradict the retrieved
   documents.

7. If the documents contain specific
   rules, dates, numbers, or requirements,
   preserve them accurately.

8. If the information is not present,
   say exactly:

   "The information was not found
   in the company documents."

Return only the final answer.
"""

        return self.llm.generate(
            prompt
        ).strip()


    # ======================================================
    # HYBRID ANSWER
    # ======================================================

    def generate_hybrid_answer(
        self,
        query,
        sql_result,
        rag_results
    ):

        # --------------------------------------------------
        # FORMAT DATABASE INFORMATION
        # --------------------------------------------------

        sql_context = (
            self.format_sql_result(
                sql_result
            )
        )

        # --------------------------------------------------
        # BUILD DOCUMENT INFORMATION
        # --------------------------------------------------

        document_context = ""

        if rag_results:

            for index, item in enumerate(
                rag_results,
                start=1
            ):

                title = (
                    item["metadata"].get(
                        "title",
                        "Company Document"
                    )
                )

                document = (
                    item["document"]
                )

                document_context += f"""
DOCUMENT {index}

Title:
{title}

Content:
{document}

"""


        # --------------------------------------------------
        # HYBRID COORDINATOR PROMPT
        # --------------------------------------------------

        prompt = f"""
You are the Hybrid Coordinator of
an enterprise AI assistant for Nova Corp.

Your job is to answer the user's question
by correctly combining TWO independent
sources:

SOURCE 1:
DATABASE / SQL

SOURCE 2:
COMPANY DOCUMENTS / RAG

You must distinguish facts from each
source and combine them only when they
are relevant.

==================================================
USER QUESTION
==================================================

{query}


==================================================
DATABASE RESULT
==================================================

{sql_context}


==================================================
COMPANY DOCUMENT CONTEXT
==================================================

{document_context}


==================================================
HYBRID ANSWERING RULES
==================================================

1. Use the database result ONLY for
   database-related facts.

2. Use company documents ONLY for
   policy, procedure, handbook, or
   other document-related information.

3. When both sources answer different
   parts of the question, combine them
   into one coherent answer.

4. Do not invent information.

5. Do not use outside knowledge.

6. Do not modify numbers from the
   database result.

7. If the database says a specific
   number, preserve that exact number.

8. If the documents contain a specific
   rule, date, requirement, or procedure,
   preserve it accurately.

9. Do NOT say that information is missing
   when the provided context actually
   contains the answer.

10. If one source does not contain the
    requested information, clearly state
    that only that part was unavailable.

11. Do not mix database facts with
    document facts.

12. For a question requiring both sources,
    clearly explain which information came
    from the company documents and which
    came from the database.

13. Keep the answer concise and easy
    to understand.

==================================================
EXPECTED ANSWER STRUCTURE
==================================================

When both sources contain useful
information, use this structure:

According to the company documents:
- [relevant policy information]

According to the database:
- [relevant database result]

Then provide a short combined conclusion
if necessary.

Return ONLY the final answer.
"""

        return self.llm.generate(
            prompt
        ).strip()
