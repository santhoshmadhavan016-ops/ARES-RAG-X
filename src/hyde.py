from llm import LLM


class HyDE:

    def __init__(self):

        self.llm = LLM()


    def generate_hypothetical_document(
        self,
        query
    ):

        prompt = f"""
You are an enterprise knowledge assistant.

Generate a short hypothetical document that could
contain the answer to the user's question.

The document should:

- Directly address the question
- Use realistic enterprise information
- Include important keywords
- Be around 3 to 5 sentences
- Do not say that you are guessing
- Do not mention this prompt
- Do not answer with a list

User question:

{query}

Hypothetical document:
"""

        hypothetical_document = self.llm.generate(
            prompt
        )

        return hypothetical_document.strip()


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    hyde = HyDE()

    test_query = (
        "What are the rules for remote access?"
    )

    print("\n")
    print("=" * 70)
    print("HyDE TEST")
    print("=" * 70)

    print("\nUSER QUESTION:")
    print(test_query)

    hypothetical_document = (
        hyde.generate_hypothetical_document(
            test_query
        )
    )

    print("\n")
    print("HYPOTHETICAL DOCUMENT:")
    print("-" * 70)

    print(hypothetical_document)

    print("\n")
    print("=" * 70)
    print("HYDE TEST COMPLETE")
    print("=" * 70)
    