import chromadb

from embedder import create_embeddings


# Where ChromaDB will store its data
CHROMA_PATH = "data/vector_db"


# Create persistent ChromaDB client
client = chromadb.PersistentClient(path=CHROMA_PATH)


# Create or load our collection
collection = client.get_or_create_collection(
    name="nova_corp_documents"
)


def store_embeddings():

    # Create chunks and embeddings
    chunks, embeddings = create_embeddings()

    # Create unique ID for every chunk
    ids = [
        f"chunk_{i}"
        for i in range(len(chunks))
    ]

    # Extract chunk text
    documents = [
        chunk["text"]
        for chunk in chunks
    ]

    # Store metadata
    metadatas = [
        {
            "title": chunk["title"],
            "filename": chunk["filename"]
        }
        for chunk in chunks
    ]

    # Convert embeddings to normal Python lists
    embedding_lists = [
        embedding.tolist()
        for embedding in embeddings
    ]

    # Store everything in ChromaDB
    collection.upsert(
        ids=ids,
        embeddings=embedding_lists,
        documents=documents,
        metadatas=metadatas
    )

    print("Embeddings stored successfully!")
    print(f"Total documents in ChromaDB: {collection.count()}")


if __name__ == "__main__":
    store_embeddings()