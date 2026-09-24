from sentence_transformers import CrossEncoder
import chromadb
from fastembed import TextEmbedding


# ============================================================
# CONFIGURATION
# ============================================================

CHROMA_PATH = "data/vector_db"

COLLECTION_NAME = "nova_corp_documents"

CROSS_ENCODER_MODEL = (
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


# ============================================================
# CONNECT TO CHROMADB
# ============================================================

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = client.get_collection(
    name=COLLECTION_NAME
)


# ============================================================
# LOAD FASTEMBED MODEL
# ============================================================

print("\nLoading FastEmbed model...")

embedding_model = TextEmbedding(
    "BAAI/bge-small-en-v1.5"
)

print("FastEmbed model loaded.")


# ============================================================
# LOAD CROSS-ENCODER
# ============================================================

print("\nLoading Cross-Encoder model...")

cross_encoder = CrossEncoder(
    CROSS_ENCODER_MODEL
)

print("Cross-Encoder model loaded.")


# ============================================================
# CROSS-ENCODER RERANKER
# ============================================================

def rerank_documents(query, top_k=5):

    print("\n")
    print("=" * 70)
    print("CROSS-ENCODER RERANKER")
    print("=" * 70)

    print("\nQuery:")
    print(query)

    # --------------------------------------------------------
    # STEP 1 — VECTOR RETRIEVAL
    # --------------------------------------------------------

    print("\nStep 1: Retrieving candidate documents...")

    query_embedding = list(
        embedding_model.embed([query])
    )[0]

    results = collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],
        n_results=10
    )

    documents = results["documents"][0]

    metadatas = results["metadatas"][0]

    print(
        f"Retrieved {len(documents)} candidate documents."
    )


    # --------------------------------------------------------
    # STEP 2 — CREATE QUERY-DOCUMENT PAIRS
    # --------------------------------------------------------

    print("\nStep 2: Creating query-document pairs...")

    pairs = []

    for document in documents:

        pairs.append(
            [query, document]
        )


    # --------------------------------------------------------
    # STEP 3 — CROSS-ENCODER SCORING
    # --------------------------------------------------------

    print("\nStep 3: Cross-Encoder scoring...")

    scores = cross_encoder.predict(
        pairs
    )


    # --------------------------------------------------------
    # STEP 4 — COMBINE DOCUMENTS AND SCORES
    # --------------------------------------------------------

    scored_documents = []

    for document, metadata, score in zip(
        documents,
        metadatas,
        scores
    ):

        scored_documents.append({

            "document": document,

            "metadata": metadata,

            "score": float(score)

        })


    # --------------------------------------------------------
    # STEP 5 — SORT BY CROSS-ENCODER SCORE
    # --------------------------------------------------------

    scored_documents.sort(
        key=lambda x: x["score"],
        reverse=True
    )


    # --------------------------------------------------------
    # STEP 6 — RETURN TOP K
    # --------------------------------------------------------

    final_results = scored_documents[:top_k]


    print(
        f"\nReturning top {len(final_results)} documents."
    )


    return final_results


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("\n")
    print("=" * 70)
    print("CROSS-ENCODER RERANKER TEST")
    print("=" * 70)


    query = (
        "What are the rules for remote access?"
    )


    results = rerank_documents(
        query,
        top_k=5
    )


    print("\n")
    print("=" * 70)
    print("FINAL RERANKED RESULTS")
    print("=" * 70)


    for index, result in enumerate(
        results,
        start=1
    ):

        print("\n")
        print("-" * 70)

        print(
            f"RESULT {index}"
        )

        print("-" * 70)

        print(
            f"Cross-Encoder Score: "
            f"{result['score']:.4f}"
        )

        print("\nTitle:")

        print(
            result["metadata"].get(
                "title",
                "Unknown"
            )
        )

        print("\nDocument:")

        print(
            result["document"]
        )