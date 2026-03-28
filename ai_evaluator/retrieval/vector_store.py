# retrieval/vector_store.py

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document


def build_vector_store(chunks, embeddings):
    """
    Builds FAISS vector store from all evidence chunks

    Each chunk must contain:
    - content
    - source
    - type (deck/video/code)
    """

    documents = []

    for chunk in chunks:
        content = chunk.get("content", "")
        source = chunk.get("source", "unknown")
        doc_type = chunk.get("type", "unknown")

        metadata = {
            "source": source,
            "type": doc_type
        }

        # Optional metadata (if available)
        if "file_path" in chunk:
            metadata["file_path"] = chunk["file_path"]

        if "timestamp" in chunk:
            metadata["timestamp"] = chunk["timestamp"]

        documents.append(
            Document(
                page_content=content,
                metadata=metadata
            )
        )

    vector_store = FAISS.from_documents(documents, embeddings)

    return vector_store


def save_vector_store(vector_store, path="vector_store"):
    """
    Persist vector store locally
    """
    vector_store.save_local(path)


def load_vector_store(path, embeddings):
    """
    Load existing vector store
    """
    return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)