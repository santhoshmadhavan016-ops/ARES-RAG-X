class QueryRouter:

    def route(self, query):

        query_lower = query.lower().strip()

        # -----------------------------------
        # DOCUMENT-ONLY QUESTIONS
        # -----------------------------------

        document_keywords = [
            "policy",
            "policies",
            "guidelines",
            "procedure",
            "process",
            "rules",
            "benefits",
            "security",
            "password",
            "suspicious email",
            "work from home",
            "leave policy",
            "attendance policy",

            # Employee handbook
            "employee handbook",
            "handbook",
            "employee responsibilities",
            "responsibilities"
        ]

        # -----------------------------------
        # SQL QUESTIONS
        # -----------------------------------

        sql_keywords = [
            "how many employees",
            "number of employees",
            "employee count",
            "employees in",
            "employees of",
            "list employees",
            "show employees",
            "salary",
            "salaries",
            "revenue",
            "sales",
            "department",
            "manager",
            "joining date",
            "designation",
            "average",
            "highest",
            "lowest",
            "total",
            "count"
        ]

        # -----------------------------------
        # CHECK KEYWORD MATCHES
        # -----------------------------------

        document_match = any(
            keyword in query_lower
            for keyword in document_keywords
        )

        sql_match = any(
            keyword in query_lower
            for keyword in sql_keywords
        )

        # -----------------------------------
        # HYBRID
        # -----------------------------------
        # If the question needs both
        # database information and
        # document information.

        if document_match and sql_match:
            return "hybrid"

        # -----------------------------------
        # DOCUMENT
        # -----------------------------------

        if document_match:
            return "document"

        # -----------------------------------
        # SQL
        # -----------------------------------

        if sql_match:
            return "sql"

        # -----------------------------------
        # DEFAULT
        # -----------------------------------

        return "document"

