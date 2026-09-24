from fastembed import TextEmbedding

from chunker import chunk_document
from document_loader import load_documents


# Load FastEmbed model
model = TextEmbedding("BAAI/bge-small-en-v1.5")


def create_embeddings():

    documents = load_documents()

    all_chunks = []

    # Create chunks from all documents
    for document in documents:

        chunks = chunk_document(document["text"])

        for chunk in chunks:
            chunk["filename"] = document["filename"]
            all_chunks.append(chunk)

    # Check chunks
    print(f"Documents loaded: {len(documents)}")
    print(f"Total chunks created: {len(all_chunks)}")

    if not all_chunks:
        raise ValueError("No chunks were created from the documents.")

    # Extract text
    texts = [chunk["text"] for chunk in all_chunks]

    # Generate embeddings
    embeddings = list(model.embed(texts))

    print(f"Embeddings created: {len(embeddings)}")

    if not embeddings:
        raise ValueError("FastEmbed returned no embeddings.")

    return all_chunks, embeddings


if __name__ == "__main__":

    chunks, embeddings = create_embeddings()

    print("\nNumber of chunks:")
    print(len(chunks))

    print("\nNumber of embeddings:")
    print(len(embeddings))

    print("\nEmbedding dimensions:")
    print(len(embeddings[0]))

    print("\nFirst chunk:")
    print(chunks[0]["title"])

    print("\nFirst embedding:")
    print(embeddings[0])