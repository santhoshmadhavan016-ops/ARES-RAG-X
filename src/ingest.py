import os
import hashlib

from pypdf import PdfReader
from docx import Document

from chunker import chunk_document
from embedder import model

import chromadb


# ============================================================
# PATHS
# ============================================================

DOCUMENTS_PATH = "data/documents"
CHROMA_PATH = "data/vector_db"


# ============================================================
# CHROMADB
# ============================================================

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = client.get_or_create_collection(
    name="nova_corp_documents"
)


# ============================================================
# LOAD TXT
# ============================================================

def load_txt(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


# ============================================================
# LOAD PDF
# ============================================================

def load_pdf(file_path):

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            text += page_text + "\n"

    return text


# ============================================================
# LOAD DOCX
# ============================================================

def load_docx(file_path):

    document = Document(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:

        if paragraph.text.strip():

            paragraphs.append(
                paragraph.text.strip()
            )

    return "\n".join(paragraphs)


# ============================================================
# UNIVERSAL DOCUMENT LOADER
# ============================================================

def load_file(file_path):

    extension = os.path.splitext(
        file_path
    )[1].lower()


    if extension == ".txt":

        return load_txt(file_path)


    elif extension == ".pdf":

        return load_pdf(file_path)


    elif extension == ".docx":

        return load_docx(file_path)


    else:

        return None


# ============================================================
# CREATE STABLE CHUNK ID
# ============================================================

def create_chunk_id(chunk):

    unique_text = (
        chunk["filename"]
        + chunk["title"]
        + chunk["text"]
    )

    chunk_id = hashlib.sha256(
        unique_text.encode("utf-8")
    ).hexdigest()

    return chunk_id


# ============================================================
# INGEST DOCUMENTS
# ============================================================

def ingest_documents():

    all_chunks = []


    print("\nScanning documents...\n")


    # --------------------------------------------------------
    # Scan document folder
    # --------------------------------------------------------

    for filename in sorted(
        os.listdir(DOCUMENTS_PATH)
    ):

        file_path = os.path.join(
            DOCUMENTS_PATH,
            filename
        )


        # Skip folders

        if not os.path.isfile(file_path):

            continue


        # ----------------------------------------------------
        # Load document
        # ----------------------------------------------------

        text = load_file(file_path)


        if not text:

            print(
                f"Skipped: {filename}"
            )

            continue


        print(
            f"Loaded: {filename}"
        )


        # ----------------------------------------------------
        # Create chunks
        # ----------------------------------------------------

        chunks = chunk_document(text)


        # ----------------------------------------------------
        # Add filename
        # ----------------------------------------------------

        for chunk in chunks:

            chunk["filename"] = filename

            all_chunks.append(chunk)


    # --------------------------------------------------------
    # Check chunks
    # --------------------------------------------------------

    print(
        f"\nTotal chunks created: {len(all_chunks)}"
    )


    if not all_chunks:

        raise ValueError(
            "No chunks were created."
        )


    # ========================================================
    # CREATE EMBEDDING TEXT
    # ========================================================

    texts = [

        f"{chunk['title']}\n{chunk['text']}"

        for chunk in all_chunks

    ]


    print(
        "Creating embeddings..."
    )


    # --------------------------------------------------------
    # Generate embeddings
    # --------------------------------------------------------

    embeddings = list(
        model.embed(texts)
    )


    print(
        f"Embeddings created: {len(embeddings)}"
    )


    # ========================================================
    # CREATE STABLE IDS
    # ========================================================

    ids = [

        create_chunk_id(chunk)

        for chunk in all_chunks

    ]


    # ========================================================
    # DOCUMENTS TO STORE
    # ========================================================

    documents = [

        f"{chunk['title']}\n{chunk['text']}"

        for chunk in all_chunks

    ]


    # ========================================================
    # METADATA
    # ========================================================

    metadatas = [

        {
            "title": chunk["title"],
            "filename": chunk["filename"]
        }

        for chunk in all_chunks

    ]


    # ========================================================
    # CONVERT EMBEDDINGS
    # ========================================================

    embedding_lists = [

        embedding.tolist()

        for embedding in embeddings

    ]


    # ========================================================
    # STORE IN CHROMADB
    # ========================================================

    collection.upsert(

        ids=ids,

        documents=documents,

        metadatas=metadatas,

        embeddings=embedding_lists

    )


    # ========================================================
    # FINAL RESULT
    # ========================================================

    print(
        "\nDocuments successfully ingested!"
    )

    print(
        f"ChromaDB total chunks: {collection.count()}"
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    ingest_documents()