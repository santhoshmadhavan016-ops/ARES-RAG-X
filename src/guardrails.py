class Guardrails:

    def __init__(self):

        self.blocked_patterns = [
            "hack",
            "hacking",
            "exploit",
            "exploitation",
            "bypass security",
            "steal password",
            "steal passwords",
            "steal a password",
            "steal a passwords",
            "delete database",
            "drop database"
        ]


    def validate_query(self, query):

        if query is None:

            return {
                "allowed": False,
                "reason": "Query cannot be empty."
            }


        query_lower = query.lower().strip()


        if not query_lower:

            return {
                "allowed": False,
                "reason": "Query cannot be empty."
            }


        # Check blocked phrases
        for pattern in self.blocked_patterns:

            if pattern in query_lower:

                return {
                    "allowed": False,
                    "reason": (
                        "The request contains a restricted "
                        "action."
                    )
                }


        # Additional password protection
        if (
            "steal" in query_lower
            and "password" in query_lower
        ):

            return {
                "allowed": False,
                "reason": (
                    "The request contains a restricted "
                    "action."
                )
            }


        return {
            "allowed": True,
            "reason": "Query accepted."
        }


    def validate_answer(self, answer):

        if answer is None:

            return {
                "allowed": False,
                "reason": "No answer was generated."
            }


        answer_lower = answer.lower().strip()


        if not answer_lower:

            return {
                "allowed": False,
                "reason": "No answer was generated."
            }


        return {
            "allowed": True,
            "reason": "Answer passed guardrails."
        }


# ==========================================================
# TEST GUARDRAILS
# ==========================================================

if __name__ == "__main__":

    guardrails = Guardrails()

    print("=" * 70)
    print("GUARDRAILS TEST")
    print("=" * 70)


    tests = [
        "How many employees are there?",
        "What is the leave policy?",
        "How can I steal a password?",
        "How can I hack the system?",
        "How can I exploit the system?",
        ""
    ]


    for query in tests:

        result = guardrails.validate_query(query)

        print("\nQuery:")
        print(query)

        print("Result:")
        print(result)