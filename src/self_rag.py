from llm import LLM
import re


class SelfRAG:

    def __init__(self):

        self.llm = LLM()


    # =====================================================
    # NORMALIZE TEXT
    # =====================================================

    def normalize_text(self, text):

        text = text.lower()

        text = re.sub(
            r"[^a-z0-9\s]",
            " ",
            text
        )

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()


    # =====================================================
    # CHECK BASIC EVIDENCE OVERLAP
    # =====================================================

    def evidence_overlap(
        self,
        answer,
        documents
    ):

        if not answer or not documents:

            return False


        answer_words = set(
            self.normalize_text(answer).split()
        )


        document_text = " ".join(
            documents
        )

        document_words = set(
            self.normalize_text(document_text).split()
        )


        if not answer_words:

            return False


        # Remove common English words
        stop_words = {
            "the",
            "a",
            "an",
            "is",
            "are",
            "was",
            "were",
            "to",
            "of",
            "and",
            "or",
            "in",
            "on",
            "for",
            "with",
            "that",
            "this",
            "it",
            "as",
            "by",
            "from",
            "be",
            "can",
            "may",
            "according"
        }


        meaningful_answer_words = (
            answer_words - stop_words
        )


        if not meaningful_answer_words:

            return False


        matched_words = (
            meaningful_answer_words
            & document_words
        )


        overlap_ratio = (
            len(matched_words)
            / len(meaningful_answer_words)
        )


        return overlap_ratio >= 0.50


    # =====================================================
    # CHECK WHETHER ANSWER IS SUPPORTED
    # =====================================================

    def evaluate_answer(
        self,
        query,
        answer,
        documents
    ):

        if not documents:

            return {
                "supported": False,
                "reason": "No documents available."
            }


        if not answer:

            return {
                "supported": False,
                "reason": "No generated answer available."
            }


        combined_documents = "\n\n".join(
            documents
        )


        prompt = f"""
You are a strict enterprise RAG fact checker.

Your ONLY task is to determine whether the
GENERATED ANSWER is supported by the
RETRIEVED DOCUMENTS.

USER QUESTION:
{query}

RETRIEVED DOCUMENTS:
{combined_documents}

GENERATED ANSWER:
{answer}

RULES:

1. Use ONLY the retrieved documents.
2. Do NOT use outside knowledge.
3. Every factual claim in the generated answer
   must be supported by the retrieved documents.
4. If the answer contains a factual claim that
   cannot be found or reasonably supported by
   the documents, return NOT_SUPPORTED.
5. Do not reject an answer merely because the
   wording is different from the documents.
6. Paraphrases are allowed when they preserve
   the meaning of the documents.
7. Do not require the exact same wording.
8. If all factual claims are supported, return
   SUPPORTED.

IMPORTANT:
Return exactly ONE label.

SUPPORTED

OR

NOT_SUPPORTED

Do not explain your decision.
Do not add punctuation.
Do not add any other words.

FINAL LABEL:
"""


        response = self.llm.generate(
            prompt
        )


        response = response.strip().upper()


        print("\nSelf-RAG Raw Verification:")
        print(response)


        # -------------------------------------------------
        # Extract explicit decision
        # -------------------------------------------------

        if "NOT_SUPPORTED" in response:

            llm_supported = False

        elif "SUPPORTED" in response:

            llm_supported = True

        else:

            llm_supported = None


        # -------------------------------------------------
        # LLM says supported
        # -------------------------------------------------

        if llm_supported is True:

            return {
                "supported": True,
                "reason": (
                    "The generated answer is supported "
                    "by the retrieved enterprise documents."
                )
            }


        # -------------------------------------------------
        # LLM says unsupported
        #
        # Use evidence check as a secondary check.
        # This prevents false rejection when the
        # answer is a close paraphrase of the source.
        # -------------------------------------------------

        if llm_supported is False:

            overlap_supported = self.evidence_overlap(
                answer,
                documents
            )


            if overlap_supported:

                return {
                    "supported": True,
                    "reason": (
                        "The answer was marked unsupported "
                        "by the verifier, but the generated "
                        "claims have sufficient evidence "
                        "overlap with the retrieved documents."
                    )
                }


            return {
                "supported": False,
                "reason": (
                    "The generated answer contains "
                    "information not sufficiently "
                    "supported by the retrieved documents."
                )
            }


        # -------------------------------------------------
        # Unclear LLM response
        # -------------------------------------------------

        overlap_supported = self.evidence_overlap(
            answer,
            documents
        )


        if overlap_supported:

            return {
                "supported": True,
                "reason": (
                    "Verifier response was unclear, but "
                    "the answer has sufficient evidence "
                    "overlap with the retrieved documents."
                )
            }


        return {
            "supported": False,
            "reason": (
                "Self-RAG returned an unclear verification "
                "result and sufficient document evidence "
                "could not be established."
            )
        }


    # =====================================================
    # REGENERATE ANSWER USING ONLY DOCUMENTS
    # =====================================================

    def regenerate_answer(
        self,
        query,
        documents
    ):

        if not documents:

            return (
                "The available enterprise documents "
                "do not provide enough information "
                "to answer this question."
            )


        combined_documents = "\n\n".join(
            documents
        )


        prompt = f"""
You are an enterprise knowledge assistant.

USER QUESTION:
{query}

ENTERPRISE DOCUMENTS:
{combined_documents}

Answer the user's question using ONLY the
information contained in the enterprise documents.

STRICT RULES:

- Do not use outside knowledge.
- Do not invent facts.
- Do not add numbers that are not present
  in the documents.
- Do not add policies that are not present.
- You may paraphrase the documents.
- If the documents do not contain enough
  information, clearly say so.
- Keep the answer concise.

ANSWER:
"""


        answer = self.llm.generate(
            prompt
        )


        return answer.strip()


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    self_rag = SelfRAG()


    # =====================================================
    # TEST 1 — SUPPORTED ANSWER
    # =====================================================

    query = (
        "What are the working hours?"
    )


    documents = [

        """
        Working Hours

        Regular working hours are 9:00 AM
        to 6:00 PM, Monday through Friday.
        """
    ]


    supported_answer = (
        "Regular working hours are "
        "9:00 AM to 6:00 PM, "
        "Monday through Friday."
    )


    print("\n")
    print("=" * 70)
    print("SELF-RAG TEST")
    print("=" * 70)


    print("\nTEST 1 — SUPPORTED ANSWER")


    result = self_rag.evaluate_answer(
        query,
        supported_answer,
        documents
    )


    print("\nQuestion:")
    print(query)


    print("\nAnswer:")
    print(supported_answer)


    print("\nSelf-RAG Result:")
    print(result)


    # =====================================================
    # TEST 2 — UNSUPPORTED ANSWER
    # =====================================================

    unsupported_answer = (
        "Regular working hours are "
        "8:00 AM to 5:00 PM, "
        "and employees receive "
        "two paid breaks."
    )


    print("\n")
    print("=" * 70)
    print("TEST 2 — UNSUPPORTED ANSWER")
    print("=" * 70)


    result = self_rag.evaluate_answer(
        query,
        unsupported_answer,
        documents
    )


    print("\nQuestion:")
    print(query)


    print("\nAnswer:")
    print(unsupported_answer)


    print("\nSelf-RAG Result:")
    print(result)


    # =====================================================
    # TEST 3 — REGENERATE
    # =====================================================

    print("\n")
    print("=" * 70)
    print("SELF-RAG REGENERATION")
    print("=" * 70)


    regenerated_answer = (
        self_rag.regenerate_answer(
            query,
            documents
        )
    )


    print("\nRegenerated Answer:")
    print(regenerated_answer)


    print("\n")
    print("=" * 70)
    print("SELF-RAG TEST COMPLETE")
    print("=" * 70)