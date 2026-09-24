import os
import sys
import re

# =========================================================
# ADD SRC FOLDER TO PYTHON PATH
# =========================================================

SRC_PATH = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from llm import LLM


class CRAG:

    def __init__(self):

        self.llm = LLM()

        # Common words that do not help determine relevance
        self.stopwords = {
            "what",
            "is",
            "are",
            "the",
            "a",
            "an",
            "for",
            "of",
            "to",
            "and",
            "in",
            "on",
            "how",
            "does",
            "do",
            "company",
            "policy",
            "please",
            "tell",
            "me",
            "about"
        }

    # =====================================================
    # TEXT NORMALIZATION
    # =====================================================

    def normalize_text(self, text):

        text = text.lower()

        words = re.findall(
            r"\b[a-zA-Z0-9]+\b",
            text
        )

        words = [
            word
            for word in words
            if word not in self.stopwords
        ]

        return set(words)

    # =====================================================
    # EVIDENCE OVERLAP
    # =====================================================

    def evidence_overlap(
        self,
        query,
        documents
    ):

        query_words = self.normalize_text(
            query
        )

        document_text = "\n\n".join(
            documents
        )

        document_words = self.normalize_text(
            document_text
        )

        if not query_words:
            return 0.0

        overlap = query_words.intersection(
            document_words
        )

        score = len(overlap) / len(query_words)

        return score

    # =====================================================
    # EVALUATE RETRIEVED DOCUMENTS
    # =====================================================

    def evaluate(
        self,
        query,
        documents
    ):

        if not documents:

            return {
                "relevant": False,
                "reason": "No documents retrieved."
            }

        # -------------------------------------------------
        # STEP 1 — EVIDENCE-BASED CHECK
        # -------------------------------------------------

        overlap_score = self.evidence_overlap(
            query,
            documents
        )

        print(
            f"\nCRAG Evidence Overlap: "
            f"{overlap_score:.2f}"
        )

        # Strong keyword evidence
        if overlap_score >= 0.50:

            return {
                "relevant": True,
                "reason": (
                    "Retrieved documents contain "
                    "sufficient query evidence."
                )
            }

        # -------------------------------------------------
        # STEP 2 — LLM RELEVANCE CHECK
        # -------------------------------------------------

        combined_documents = "\n\n".join(
            documents
        )

        prompt = f"""
You are a retrieval quality evaluator
for an enterprise RAG system.

User Question:
{query}

Retrieved Documents:
{combined_documents}

Determine whether the retrieved documents
contain information that can directly help
answer the user's question.

Important rules:

- Judge the actual retrieved documents.
- Do not require exact wording.
- Accept reasonable paraphrases.
- If the document clearly discusses the same
  topic as the user question, consider it relevant.
- Do not reject a document simply because it
  does not contain every word from the question.

Return ONLY one of these:

RELEVANT

or

NOT_RELEVANT

Do not provide an explanation.
"""

        response = self.llm.generate(
            prompt
        )

        response = response.strip().upper()

        print(
            "\nCRAG Raw Verification:"
        )

        print(response)

        # -------------------------------------------------
        # STEP 3 — PROCESS LLM RESULT
        # -------------------------------------------------

        if "NOT_RELEVANT" in response:

            return {
                "relevant": False,
                "reason": (
                    "Retrieved documents are "
                    "not sufficiently relevant."
                )
            }

        if "RELEVANT" in response:

            return {
                "relevant": True,
                "reason": (
                    "Retrieved documents are relevant."
                )
            }

        # -------------------------------------------------
        # STEP 4 — UNCLEAR RESULT
        # -------------------------------------------------

        return {
            "relevant": False,
            "reason": (
                "CRAG could not confidently "
                "evaluate the documents."
            )
        }

    # =====================================================
    # GENERATE CORRECTIVE QUERY
    # =====================================================

    def generate_corrective_query(
        self,
        query,
        documents
    ):

        combined_documents = "\n\n".join(
            documents
        )

        prompt = f"""
You are a query reformulation system
for an enterprise RAG application.

Original User Question:
{query}

Retrieved Documents:
{combined_documents}

The retrieved documents are not relevant
enough to answer the user's question.

Create a better search query that can be
used to retrieve the correct enterprise
document.

Requirements:

- Preserve the user's original intent.
- Add useful keywords.
- Be specific.
- Do not invent company facts.
- Return ONLY the improved search query.
"""

        improved_query = self.llm.generate(
            prompt
        )

        return improved_query.strip()


# =========================================================
# CRAG TEST
# =========================================================

if __name__ == "__main__":

    crag = CRAG()

    # =====================================================
    # TEST 1 — RELEVANT DOCUMENT
    # =====================================================

    query = (
        "What are the rules for remote access?"
    )

    documents = [

        """
        Remote Access

        Employees accessing company systems
        remotely must use the approved secure
        connection provided by Nova Corp.

        Public or unsecured networks should
        not be used for sensitive company
        operations.
        """
    ]

    print("\n")
    print("=" * 70)
    print("CRAG CORRECTIVE RETRIEVAL TEST")
    print("=" * 70)

    print("\n")
    print("TEST 1 — RELEVANT DOCUMENT")

    result = crag.evaluate(
        query,
        documents
    )

    print("\nCRAG RESULT:")
    print(result)

    # =====================================================
    # TEST 2 — IRRELEVANT DOCUMENTS
    # =====================================================

    bad_query = (
        "What are the rules for remote access?"
    )

    bad_documents = [

        """
        Annual Leave

        Full-time employees are eligible
        for annual paid leave according to
        their employment category.
        """,

        """
        Working Hours

        Regular working hours are
        9:00 AM to 6:00 PM,
        Monday through Friday.
        """
    ]

    print("\n")
    print("=" * 70)
    print("TEST 2 — IRRELEVANT DOCUMENTS")
    print("=" * 70)

    bad_result = crag.evaluate(
        bad_query,
        bad_documents
    )

    print("\nCRAG RESULT:")
    print(bad_result)

    # =====================================================
    # CORRECTIVE QUERY
    # =====================================================

    if not bad_result["relevant"]:

        improved_query = (
            crag.generate_corrective_query(
                bad_query,
                bad_documents
            )
        )

        print("\n")
        print("=" * 70)
        print("CORRECTIVE QUERY")
        print("=" * 70)

        print("\nOriginal Query:")
        print(bad_query)

        print("\nImproved Query:")
        print(improved_query)

    print("\n")
    print("=" * 70)
    print("CRAG CORRECTIVE RETRIEVAL TEST COMPLETE")
    print("=" * 70)
