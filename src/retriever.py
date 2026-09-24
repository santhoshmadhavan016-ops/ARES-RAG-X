import re

import chromadb
from fastembed import TextEmbedding

from hyde import HyDE
from CRAG.crag import CRAG
from reranker import rerank_documents


# ============================================================
# CONFIGURATION
# ============================================================

CHROMA_PATH = "data/vector_db"


# ============================================================
# CONNECT TO CHROMADB
# ============================================================

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = client.get_collection(
    name="nova_corp_documents"
)


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

model = TextEmbedding(
    "BAAI/bge-small-en-v1.5"
)


# ============================================================
# INITIALIZE HYDE + CRAG
# ============================================================

hyde = HyDE()

crag = CRAG()


# ============================================================
# TOKENIZATION
# ============================================================

def tokenize(text):

    text = text.lower()

    words = re.findall(
        r"\b[a-zA-Z0-9]+\b",
        text
    )

    return set(words)


# ============================================================
# NORMALIZE TERMS
# ============================================================

def normalize_terms(text):

    text = text.lower()

    replacements = {

        "working remotely":
            "remote access",

        "remote working":
            "remote access",

        "work remotely":
            "remote access",

        "classified":
            "classification",

        "classify":
            "classification",

        "classifying":
            "classification",

        "leaves":
            "offboarding",

        "leaving":
            "offboarding",

        "leaved":
            "offboarding",

        "company assets":
            "assets",

        "corporate assets":
            "assets"
    }

    for old, new in replacements.items():

        text = text.replace(
            old,
            new
        )

    return text


# ============================================================
# KEYWORD SCORE
# ============================================================

def keyword_score(
    query,
    title,
    document
):

    query = normalize_terms(
        query
    )

    title = normalize_terms(
        title
    )

    document = normalize_terms(
        document
    )

    query_words = tokenize(
        query
    )

    title_words = tokenize(
        title
    )

    document_words = tokenize(
        document
    )

    if not query_words:

        return 0.0

    title_matches = (
        query_words &
        title_words
    )

    document_matches = (
        query_words &
        document_words
    )

    title_score = (
        len(title_matches)
        /
        len(query_words)
    )

    document_score = (
        len(document_matches)
        /
        len(query_words)
    )

    score = (
        0.70 * title_score
        +
        0.30 * document_score
    )

    return score


# ============================================================
# INTENT BOOST
# ============================================================

def intent_boost(
    query,
    title,
    filename
):

    query = normalize_terms(
        query
    ).lower()

    title = normalize_terms(
        title
    ).lower()

    filename = filename.lower()

    boost = 0.0

    if (
        "remote access" in query
        and
        (
            "remote access" in title
            or
            "remote_access" in filename
        )
    ):

        boost += 0.30


    if (
        "classification" in query
        and
        (
            "information classification"
            in title

            or

            "information_classification"
            in filename
        )
    ):

        boost += 0.30


    if (
        "offboarding" in query
        and
        (
            "offboarding" in title
            or
            "offboarding" in filename
        )
    ):

        boost += 0.30


    return boost


# ============================================================
# HYBRID CANDIDATE SEARCH
# ============================================================

def search_documents(
    search_query,
    original_query,
    top_k=10
):

    print("\n")
    print("=" * 70)
    print("VECTOR SEARCH")
    print("=" * 70)

    print("\nSearch Query:")
    print(search_query)


    # --------------------------------------------------------
    # VECTOR SEARCH
    # --------------------------------------------------------

    query_embedding = list(
        model.embed(
            [search_query]
        )
    )[0]


    query_embedding_list = (
        query_embedding.tolist()
    )


    results = collection.query(

        query_embeddings=[
            query_embedding_list
        ],

        n_results=10
    )


    documents = results[
        "documents"
    ][0]


    metadatas = results[
        "metadatas"
    ][0]


    print(
        "\nVector candidates:"
        f" {len(documents)}"
    )


    # --------------------------------------------------------
    # PRE-RANK USING EXISTING SIGNALS
    # --------------------------------------------------------

    candidate_documents = []


    document_embeddings = list(
        model.embed(documents)
    )


    for (
        document,
        metadata,
        embedding
    ) in zip(
        documents,
        metadatas,
        document_embeddings
    ):

        semantic_score = sum(

            q * d

            for q, d in zip(
                query_embedding,
                embedding
            )
        )


        title = metadata.get(
            "title",
            ""
        )


        filename = metadata.get(
            "filename",
            ""
        )


        keyword = keyword_score(

            original_query,

            title,

            document
        )


        boost = intent_boost(

            original_query,

            title,

            filename
        )


        preliminary_score = (

            0.65 *
            semantic_score

            +

            0.25 *
            keyword

            +

            boost
        )


        candidate_documents.append({

            "document":
                document,

            "metadata":
                metadata,

            "semantic_score":
                semantic_score,

            "keyword_score":
                keyword,

            "intent_boost":
                boost,

            "preliminary_score":
                preliminary_score
        })


    # --------------------------------------------------------
    # PRE-RANK TOP 10
    # --------------------------------------------------------

    candidate_documents.sort(

        key=lambda x:
            x["preliminary_score"],

        reverse=True
    )


    candidate_documents = (
        candidate_documents[:10]
    )


    return candidate_documents


# ============================================================
# CROSS-ENCODER RERANKING
# ============================================================

def cross_encoder_rerank(
    query,
    candidates,
    top_k=5
):

    print("\n")
    print("=" * 70)
    print("CROSS-ENCODER RERANKING")
    print("=" * 70)


    if not candidates:

        return []


    documents = [

        item["document"]

        for item in candidates
    ]


    # --------------------------------------------------------
    # CROSS-ENCODER
    # --------------------------------------------------------

    from sentence_transformers import CrossEncoder


    reranker_model = CrossEncoder(
        "cross-encoder/ms-marco-MiniLM-L-6-v2"
    )


    pairs = [

        [query, document]

        for document in documents
    ]


    scores = reranker_model.predict(
        pairs
    )


    reranked = []


    for (
        item,
        score
    ) in zip(
        candidates,
        scores
    ):

        result = item.copy()

        result[
            "cross_encoder_score"
        ] = float(score)

        result[
            "score"
        ] = float(score)

        reranked.append(
            result
        )


    reranked.sort(

        key=lambda x:
            x["cross_encoder_score"],

        reverse=True
    )


    final_results = (
        reranked[:top_k]
    )


    print(
        "\nCross-Encoder ranking:"
    )


    for index, result in enumerate(

        final_results,

        start=1

    ):

        print(

            f"{index}. "

            f"{result['metadata'].get('title', 'Unknown')} "

            f"→ "

            f"{result['cross_encoder_score']:.4f}"
        )


    return final_results


# ============================================================
# COMPLETE RETRIEVAL + RERANKING
# ============================================================

def retrieve_and_rerank(
    query,
    top_k=5
):

    print("\n")
    print("=" * 70)
    print("HYDE")
    print("=" * 70)

    print("\nOriginal Query:")
    print(query)


    # --------------------------------------------------------
    # HYDE
    # --------------------------------------------------------

    hypothetical_document = (
        hyde.generate_hypothetical_document(
            query
        )
    )


    print(
        "\nHypothetical Document:"
    )

    print("-" * 70)

    print(
        hypothetical_document
    )


    # --------------------------------------------------------
    # VECTOR SEARCH
    # --------------------------------------------------------

    candidates = search_documents(

        search_query=
            hypothetical_document,

        original_query=
            query,

        top_k=10
    )


    # --------------------------------------------------------
    # CROSS-ENCODER
    # --------------------------------------------------------

    reranked_results = (
        cross_encoder_rerank(

            query,

            candidates,

            top_k
        )
    )


    # --------------------------------------------------------
    # CRAG
    # --------------------------------------------------------

    print("\n")
    print("=" * 70)
    print("CRAG EVALUATION")
    print("=" * 70)


    documents = [

        result["document"]

        for result in reranked_results
    ]


    crag_result = crag.evaluate(

        query,

        documents
    )


    print("\nQuestion:")
    print(query)


    print("\nCRAG Result:")
    print(
        crag_result["relevant"]
    )


    print("\nReason:")
    print(
        crag_result["reason"]
    )


    # --------------------------------------------------------
    # RELEVANT
    # --------------------------------------------------------

    if crag_result["relevant"]:

        print("\n")
        print("=" * 70)
        print(
            "CRAG: DOCUMENTS ARE RELEVANT"
        )
        print("=" * 70)

        print(
            "\nUsing Cross-Encoder reranked results."
        )

        return reranked_results


    # --------------------------------------------------------
    # CORRECTIVE RETRIEVAL
    # --------------------------------------------------------

    print("\n")
    print("=" * 70)
    print(
        "CRAG: CORRECTIVE RETRIEVAL"
    )
    print("=" * 70)

    print(
        "\nInitial retrieval was not relevant enough."
    )


    improved_query = (
        crag.generate_corrective_query(

            query,

            documents
        )
    )


    print("\nOriginal Query:")
    print(query)


    print("\nCorrective Query:")
    print(improved_query)


    corrected_candidates = (
        search_documents(

            search_query=
                improved_query,

            original_query=
                query,

            top_k=10
        )
    )


    corrected_results = (
        cross_encoder_rerank(

            query,

            corrected_candidates,

            top_k
        )
    )


    # --------------------------------------------------------
    # SECOND CRAG
    # --------------------------------------------------------

    corrected_documents = [

        result["document"]

        for result in corrected_results
    ]


    print("\n")
    print("=" * 70)
    print("CRAG SECOND EVALUATION")
    print("=" * 70)


    second_crag_result = (
        crag.evaluate(

            query,

            corrected_documents
        )
    )


    print(
        "\nSecond CRAG Result:"
    )

    print(
        second_crag_result["relevant"]
    )


    print("\nReason:")

    print(
        second_crag_result["reason"]
    )


    print("\n")
    print("=" * 70)
    print(
        "CORRECTIVE RETRIEVAL COMPLETE"
    )
    print("=" * 70)


    return corrected_results