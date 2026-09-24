from pathlib import Path


DOCUMENTS_DIR = Path("data/documents")


def load_documents():
    documents = []

    for file_path in DOCUMENTS_DIR.iterdir():

        if file_path.is_file() and file_path.suffix.lower() == ".txt":

            text = file_path.read_text(encoding="utf-8")

            documents.append({
                "filename": file_path.name,
                "text": text
            })

    return documents


if __name__ == "__main__":
    documents = load_documents()

    print(f"Loaded {len(documents)} document(s)\n")

    for document in documents:
        print("=" * 60)
        print(f"FILE: {document['filename']}")
        print("=" * 60)
        print(document["text"][:500])
        print()