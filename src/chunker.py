from document_loader import load_documents


def chunk_document(text):
    chunks = []

    current_title = None
    current_content = []

    for line in text.splitlines():

        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Skip the main document title
        if line.startswith("NOVA CORP"):
            continue

        # Detect section headings
        # A heading is a short line without a period at the end.
        # Examples:
        # Working Schedule
        # Attendance Recording
        # Late Arrival
        if (
            len(line) < 100
            and not line.endswith(".")
            and not line.endswith(":")
        ):

            # Save previous section
            if current_title and current_content:
                chunks.append({
                    "title": current_title,
                    "text": "\n".join(current_content).strip()
                })

            # Start new section
            current_title = line
            current_content = []

        else:

            # Add normal content to current section
            if current_title:
                current_content.append(line)

    # Save final section
    if current_title and current_content:
        chunks.append({
            "title": current_title,
            "text": "\n".join(current_content).strip()
        })

    return chunks


if __name__ == "__main__":

    documents = load_documents()

    for document in documents:

        chunks = chunk_document(document["text"])

        print(f"\nDocument: {document['filename']}")
        print(f"Number of chunks: {len(chunks)}\n")

        for i, chunk in enumerate(chunks, start=1):

            print("=" * 60)
            print(f"CHUNK {i}")
            print(f"TITLE: {chunk['title']}")
            print("=" * 60)
            print(chunk["text"])
            print()