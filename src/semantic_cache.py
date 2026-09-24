import json
import os
import re

import numpy as np
from sentence_transformers import SentenceTransformer


class SemanticCache:

    def __init__(
        self,
        cache_file="data/semantic_cache.json",
        similarity_threshold=0.80
    ):

        self.cache_file = cache_file

        self.similarity_threshold = (
            similarity_threshold
        )

        print(
            "\nLoading semantic cache "
            "embedding model..."
        )

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        print(
            "Semantic cache model loaded."
        )

        os.makedirs(
            os.path.dirname(
                self.cache_file
            ),
            exist_ok=True
        )

        self.cache = self._load_cache()


    # ======================================================
    # LOAD CACHE
    # ======================================================

    def _load_cache(self):

        if not os.path.exists(
            self.cache_file
        ):
            return []

        try:

            with open(
                self.cache_file,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)


            if isinstance(data, dict):

                converted_cache = []

                for key, value in data.items():

                    converted_cache.append(
                        value
                    )

                return converted_cache


            return data


        except (
            json.JSONDecodeError,
            OSError
        ):

            return []


    # ======================================================
    # SAVE CACHE
    # ======================================================

    def _save_cache(self):

        with open(
            self.cache_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.cache,
                file,
                indent=4,
                ensure_ascii=False
            )


    # ======================================================
    # CREATE EMBEDDING
    # ======================================================

    def _create_embedding(
        self,
        question
    ):

        embedding = self.model.encode(
            question
        )

        return embedding.tolist()


    # ======================================================
    # COSINE SIMILARITY
    # ======================================================

    def _cosine_similarity(
        self,
        embedding_a,
        embedding_b
    ):

        vector_a = np.array(
            embedding_a
        )

        vector_b = np.array(
            embedding_b
        )

        norm_a = np.linalg.norm(
            vector_a
        )

        norm_b = np.linalg.norm(
            vector_b
        )

        if (
            norm_a == 0
            or norm_b == 0
        ):

            return 0.0


        similarity = (
            np.dot(
                vector_a,
                vector_b
            )
            /
            (
                norm_a
                *
                norm_b
            )
        )

        return float(
            similarity
        )


    # ======================================================
    # EXTRACT QUESTION TERMS
    # ======================================================

    def _extract_terms(
        self,
        question
    ):

        question = question.lower()

        words = re.findall(
            r"\b[a-zA-Z0-9]+\b",
            question
        )

        stop_words = {
            "what",
            "are",
            "is",
            "the",
            "a",
            "an",
            "how",
            "many",
            "does",
            "do",
            "there",
            "company",
            "can",
            "could",
            "would",
            "should",
            "tell",
            "me",
            "about",
            "please",
            "and",
            "or",
            "of",
            "to",
            "for",
            "in",
            "on",
            "with"
        }

        terms = {
            word
            for word in words
            if word not in stop_words
        }

        return terms


    # ======================================================
    # TERM COMPATIBILITY
    # ======================================================

    def _term_compatibility(
        self,
        question_a,
        question_b
    ):

        terms_a = self._extract_terms(
            question_a
        )

        terms_b = self._extract_terms(
            question_b
        )


        if not terms_a or not terms_b:

            return 0.0


        common_terms = (
            terms_a & terms_b
        )


        # ----------------------------------------------
        # Jaccard similarity
        # ----------------------------------------------

        union_terms = (
            terms_a | terms_b
        )

        if not union_terms:

            return 0.0


        jaccard = (
            len(common_terms)
            /
            len(union_terms)
        )


        # ----------------------------------------------
        # Coverage
        # ----------------------------------------------

        coverage_a = (
            len(common_terms)
            /
            len(terms_a)
        )

        coverage_b = (
            len(common_terms)
            /
            len(terms_b)
        )


        # ----------------------------------------------
        # Compatibility
        #
        # We want similar questions to share
        # the same important concepts.
        # ----------------------------------------------

        compatibility = min(
            coverage_a,
            coverage_b
        )


        # Combine Jaccard and coverage
        final_score = (
            0.5 * jaccard
            +
            0.5 * compatibility
        )


        return final_score


    # ======================================================
    # CHECK QUERY COMPATIBILITY
    # ======================================================

    def _is_compatible(
        self,
        current_question,
        cached_question
    ):

        current_terms = self._extract_terms(
            current_question
        )

        cached_terms = self._extract_terms(
            cached_question
        )


        # ----------------------------------------------
        # If current question has additional
        # important concepts, do not reuse a
        # narrower cached answer.
        # ----------------------------------------------

        if (
            current_terms
            and cached_terms
        ):

            missing_from_cache = (
                current_terms
                - cached_terms
            )


            if missing_from_cache:

                print(
                    "\nCache compatibility:"
                    " FAILED"
                )

                print(
                    "New question contains "
                    "additional concepts:"
                )

                print(
                    missing_from_cache
                )

                return False


        compatibility = (
            self._term_compatibility(
                current_question,
                cached_question
            )
        )


        print(
            "\nCache term compatibility:"
            f" {compatibility:.4f}"
        )


        # ----------------------------------------------
        # Require reasonable concept overlap
        # ----------------------------------------------

        if compatibility >= 0.50:

            return True


        return False


    # ======================================================
    # GET FROM CACHE
    # ======================================================

    def get(
        self,
        question
    ):

        if not self.cache:

            return None


        question_embedding = (
            self._create_embedding(
                question
            )
        )


        best_match = None

        best_similarity = 0.0


        # ==================================================
        # SEARCH CACHE
        # ==================================================

        for item in self.cache:

            cached_embedding = (
                item.get("embedding")
            )


            # ----------------------------------------------
            # Old cache entries may not contain embeddings
            # ----------------------------------------------

            if not cached_embedding:

                continue


            similarity = (
                self._cosine_similarity(
                    question_embedding,
                    cached_embedding
                )
            )


            print(
                "\nCached Question:"
            )

            print(
                item.get(
                    "question",
                    ""
                )
            )

            print(
                "Semantic Similarity:"
                f" {similarity:.4f}"
            )


            if similarity > best_similarity:

                best_similarity = similarity

                best_match = item


        print(
            "\nBest cache similarity:"
            f" {best_similarity:.4f}"
        )


        # ==================================================
        # SEMANTIC THRESHOLD
        # ==================================================

        if (
            best_match is None
            or best_similarity
            < self.similarity_threshold
        ):

            print(
                "Similarity threshold not reached:"
                f" {self.similarity_threshold}"
            )

            return None


        print(
            "Similarity threshold passed:"
            f" {self.similarity_threshold}"
        )


        # ==================================================
        # COMPATIBILITY CHECK
        # ==================================================

        cached_question = (
            best_match.get(
                "question",
                ""
            )
        )


        compatible = (
            self._is_compatible(
                question,
                cached_question
            )
        )


        if not compatible:

            print(
                "\nCACHE REJECTED"
            )

            print(
                "Reason: semantic similarity "
                "was high, but question concepts "
                "are not compatible."
            )

            return None


        # ==================================================
        # CACHE HIT
        # ==================================================

        print(
            "\nCACHE ACCEPTED"
        )

        return {
            "question": cached_question,

            "answer": best_match.get(
                "answer",
                ""
            ),

            "similarity": best_similarity
        }


    # ======================================================
    # SET CACHE
    # ======================================================

    def set(
        self,
        question,
        answer
    ):

        embedding = (
            self._create_embedding(
                question
            )
        )


        cache_entry = {

            "question": question,

            "answer": answer,

            "embedding": embedding

        }


        self.cache.append(
            cache_entry
        )


        self._save_cache()


    # ======================================================
    # CLEAR CACHE
    # ======================================================

    def clear(self):

        self.cache = []

        self._save_cache()


    # ======================================================
    # CACHE SIZE
    # ======================================================

    def size(self):

        return len(
            self.cache
        )
